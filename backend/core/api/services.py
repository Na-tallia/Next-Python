import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from .models import Ad


# Загружаем переменные из .env
load_dotenv()
TOKEN = os.getenv("META_ACCESS_TOKEN")


def _parse_datetime(value: str | None):
    """Безопасно парсим ISO-дату Meta в datetime или возвращаем None."""
    if not value:
        return None
    try:
        # Meta обычно возвращает даты в формате 2024-01-01T12:00:00+0000 или с Z
        value = value.replace("Z", "+00:00")
        # Нормализуем странный формат смещения +0000 → +00:00
        if len(value) > 5 and (value[-5] in {"+", "-"} and value[-3] != ":"):
            value = value[:-2] + ":" + value[-2:]
        return datetime.fromisoformat(value)
    except Exception:
        return None


def fetch_and_save_ads(search_terms: str = "real estate Greece"):
    """
    Забирает объявления из Meta Ads Library и сохраняет/обновляет их в модели Ad.
    """
    if not TOKEN:
        return "Ошибка: META_ACCESS_TOKEN не задан в .env"

    url = "https://graph.facebook.com/v19.0/ads_archive"
    params = {
        "access_token": TOKEN,
        # Ищем объявления по недвижимости, фокус на Греции
        "search_terms": search_terms,
        "ad_type": "all",
        "ad_active_status": "ACTIVE",  # только активные объявления
        "ad_reached_countries": "['GR']",  # Греция
        "limit": 50,
        "fields": (
            "id,ad_snapshot_url,page_id,page_name,"
            "ad_creative_bodies,publisher_platforms,"
            "ad_delivery_start_time,ad_delivery_stop_time,languages"
        ),
    }

    response = requests.get(url, params=params)
    data = response.json()

    items = data.get("data", [])
    if not items:
        return f"Ошибка: {data.get('error')}" if data.get("error") else "Объявлений не найдено"

    for item in items:
        ad_id = item.get("id")
        if not ad_id:
            continue

        ad_creative_bodies = item.get("ad_creative_bodies") or [None]

        Ad.objects.update_or_create(
            ad_id=ad_id,
            defaults={
                "page_id": item.get("page_id"),
                "page_name": item.get("page_name"),
                "start_time": _parse_datetime(item.get("ad_delivery_start_time")),
                "stop_time": _parse_datetime(item.get("ad_delivery_stop_time")),
                "ad_text": ad_creative_bodies[0],
                "snapshot_url": item.get("ad_snapshot_url"),
                "publisher_platforms": item.get("publisher_platforms") or [],
                "languages": item.get("languages") or [],
                "raw_ads": item,
            },
        )

    return f"Успешно сохранено {len(items)} объявлений"
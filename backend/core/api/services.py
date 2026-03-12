import os
import requests
from dotenv import load_dotenv
from .models import Ad

# Загружаем переменные из .env
load_dotenv()
TOKEN = os.getenv('META_ACCESS_TOKEN')

def fetch_and_save_ads(search_terms='shopping'):
    url = "https://graph.facebook.com/v19.0/ads_archive"
    params = {
        'access_token': TOKEN,
        'search_terms': search_terms,
        'ad_reached_countries': "['BY']", # Можно поменять на нужные страны
        'fields': 'ad_snapshot_url,page_id,page_name,ad_creative_bodies,publisher_platforms'
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    if 'data' in data:
        for item in data['data']:
            Ad.objects.update_or_create(
                ad_id=item.get('id'),
                defaults={
                    'page_id': item.get('page_id'),
                    'page_name': item.get('page_name'),
                    'ad_text': item.get('ad_creative_bodies', [None])[0],
                    'snapshot_url': item.get('ad_snapshot_url'),
                    'publisher_platforms': item.get('publisher_platforms', [])
                }
            )
        return f"Успешно сохранено {len(data['data'])} объявлений"
    return f"Ошибка: {data.get('error')}"
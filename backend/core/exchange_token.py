import os
from getpass import getpass

import requests
from dotenv import load_dotenv


def main() -> None:
    # Загружаем переменные окружения из .env рядом с этим файлом
    load_dotenv()

    access_token = os.getenv("META_ACCESS_TOKEN")
    app_id = os.getenv("META_APP_ID")
    app_secret_env = os.getenv("META_APP_SECRET")

    if not access_token:
        print("❌ META_ACCESS_TOKEN не найден в .env")
        return

    if not app_id:
        print("❌ META_APP_ID не найден в .env")
        return

    # Секрет по умолчанию берём из .env, чтобы избежать опечаток
    if app_secret_env:
        app_secret = app_secret_env.strip()
    else:
        app_secret = getpass("Введите META_APP_SECRET (секрет приложения Meta): ").strip()
        if not app_secret:
            print("❌ META_APP_SECRET не введён")
            return

    url = "https://graph.facebook.com/v19.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": access_token,
    }

    print("🔄 Обмениваем краткосрочный токен на долгосрочный...")
    response = requests.get(url, params=params)

    try:
        data = response.json()
    except Exception:
        print("❌ Не удалось распарсить ответ Meta:", response.text)
        return

    if "access_token" in data:
        long_lived_token = data["access_token"]
        expires_in = data.get("expires_in")
        print("✅ Долгосрочный токен (примерно на 60 дней):")
        print(long_lived_token)
        if expires_in is not None:
            print(f"⏳ Истекает через ~{expires_in} секунд")
    else:
        print("❌ Ошибка при обмене токена:")
        print(data)


if __name__ == "__main__":
    main()


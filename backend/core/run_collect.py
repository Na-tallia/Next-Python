import os
import django
from dotenv import load_dotenv

# 1. Загружаем переменные из .env ДО всего остального
load_dotenv()

# 2. Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.services import fetch_and_save_ads

if __name__ == "__main__":
    # Проверка: печатаем кусочек токена в консоль, чтобы убедиться, что он считался
    token = os.getenv('META_ACCESS_TOKEN')
    if token:
        print(f"📡 Токен найден: {token[:10]}...")
        # Запускаем сбор: функция сама возьмёт токен из .env
        result = fetch_and_save_ads('бизнес')
        print(f"📊 Результат: {result}")
    else:
        print("❌ Ошибка: META_ACCESS_TOKEN не найден в .env файле!")
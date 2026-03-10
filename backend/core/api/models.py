from django.db import models


class Ad(models.Model):
    # ad_id используем как Primary Key (уникальный паспорт объявления)
    ad_id = models.CharField(max_length=100, unique=True, primary_key=True)
    
    # Информация о странице
    page_id = models.CharField(max_length=100)
    page_name = models.CharField(max_length=255)
    
    # Даты показа
    start_time = models.DateTimeField(null=True, blank=True)
    stop_time = models.DateTimeField(null=True, blank=True)
    
    # Содержание
    ad_text = models.TextField(null=True, blank=True)
    snapshot_url = models.URLField(max_length=1000, null=True, blank=True)
    
    # Платформы и языки храним в JSON (удобно для списков)
    publisher_platforms = models.JSONField(default=list)
    languages = models.JSONField(default=list)
    
    # Поле для хранения всего ответа от Meta (на всякий случай)
    raw_ads = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.page_name} | {self.ad_id}"
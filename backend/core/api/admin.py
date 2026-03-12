from django.contrib import admin
from .models import Ad

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    # Эти колонки будут видны в списке всех объявлений
    list_display = ('ad_id', 'page_name', 'start_time', 'stop_time')
    # По этим полям можно будет искать
    search_fields = ('ad_id', 'page_name')
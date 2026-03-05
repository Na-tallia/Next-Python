from django.db import models

# Create your models here.
from django.db import models

class Todo(models.Model):
    # Заголовок задачи (короткий текст до 200 символов)
    title = models.CharField(max_length=200)
    # Описание (длинный текст, может быть пустым)
    description = models.TextField(blank=True)
    # Статус: выполнено (True) или нет (False)
    completed = models.BooleanField(default=False)
    # Время создания задачи (ставится автоматически)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
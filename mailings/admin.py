from django.contrib import admin

from .models import Message


# Register your models here.
@admin.register(Message)
class Message(admin.ModelAdmin):
    """
    Класс для отображения модели Message в интерфейсе админки
    """
    list_display = ("id", "subject")

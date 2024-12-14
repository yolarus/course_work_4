from django.contrib import admin

from .models import Message, Recipient


# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Класс для отображения модели Message в интерфейсе админки
    """
    list_display = ("id", "subject")


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    """
    Класс для отображения модели Recipient в интерфейсе админки
    """
    list_display = ("id", "email")

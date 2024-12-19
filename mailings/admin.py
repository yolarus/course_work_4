from django.contrib import admin

from .models import AttemptMailing, Mailing, Message, Recipient


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


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """
    Класс для отображения модели Mailing в интерфейсе админки
    """
    list_display = ("id", "status")


@admin.register(AttemptMailing)
class AttemptMailingAdmin(admin.ModelAdmin):
    """
    Класс для отображения модели AttemptMailing в интерфейсе админки
    """
    list_display = ("id", "status")

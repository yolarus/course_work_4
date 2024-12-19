from django.core.management import call_command
from django.core.management.base import BaseCommand

from config import main_logger
from mailings.models import Mailing, Message, Recipient


class Command(BaseCommand):
    """
    Заполнение БД фикстурой сообщений, получателей, рассылок и их попыток сервиса рассылок
    """

    def handle(self, *args: list, **kwargs: dict) -> None:
        main_logger.info("Запущена кастомная команда load_mailings")

        Mailing.objects.all().delete()
        Message.objects.all().delete()
        Recipient.objects.all().delete()

        call_command('loaddata', 'mailings.json')

        self.stdout.write(self.style.SUCCESS("Фикстуры из файла mailing.json успешно загружены"))
        main_logger.info("Фикстуры из файла mailing_fixture.json успешно загружены")

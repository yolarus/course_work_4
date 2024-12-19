from django.core.management import BaseCommand

from src.scheduler import start_scheduler


class Command(BaseCommand):
    """
    Автоматическая отправка рассылок по расписанию
    """
    def handle(self, *args, **options):
        start_scheduler()

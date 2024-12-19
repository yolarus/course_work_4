from django.core.management import BaseCommand

from config import main_logger
from src.scheduler import start_scheduler


class Command(BaseCommand):
    """
    Автоматическая отправка рассылок по расписанию
    """
    def handle(self, *args, **options):
        main_logger.info("Запущена кастомная команда start_scheduler")
        start_scheduler()

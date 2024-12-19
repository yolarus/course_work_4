from django.core.management import BaseCommand

from config import main_logger
from src.utils import send_mailing
from users.models import User

user = User.objects.get(email="admin@mail.ru")


class Command(BaseCommand):
    """
    Отправка рассылки сообщений по id
    """
    def handle(self, *args, **options):
        main_logger.info(f"Запущена кастомная команда send_mailing {options['mailing_id']}")

        mail_server_response = send_mailing(options["mailing_id"], user)
        if mail_server_response != "Рассылка успешно отправлена":
            self.stdout.write(self.style.ERROR(mail_server_response))
        else:
            self.stdout.write(self.style.SUCCESS(mail_server_response))

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, action="store", help="id рассылки сообщений Mailing")

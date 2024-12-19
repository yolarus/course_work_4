from django.core.management import BaseCommand

from src.utils import send_mailing
from users.models import User

user = User.objects.get(email="admin@mail.ru")


class Command(BaseCommand):
    """
    Отправка рассылки сообщений по id
    """
    def handle(self, *args, **options):
        mail_server_response = send_mailing(options["mailing_id"], user)
        if mail_server_response != "Рассылка успешно отправлена":
            self.stdout.write(self.style.ERROR(mail_server_response))
        else:
            self.stdout.write(self.style.SUCCESS(mail_server_response))

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, action="store", help="id рассылки сообщений Mailing")

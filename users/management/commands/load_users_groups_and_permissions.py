from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand

from config import main_logger
from users.models import User


class Command(BaseCommand):
    """
    Заполнение БД пользователями, группами и разрешениями
    """

    def handle(self, *args: list, **kwargs: dict) -> None:
        main_logger.info("Запущена кастомная команда load_users_group_and_permissions")

        User.objects.all().delete()
        Group.objects.all().delete()
        call_command('loaddata', 'groups_and_permissions.json')
        call_command('loaddata', 'users.json')

        self.stdout.write(self.style.SUCCESS("Фикстуры из файлов groups_and_permissions.json и "
                                             "users.json успешно загружены"))
        main_logger.info("Фикстуры из файлов groups_and_permissions.json и users.json успешно загружены")

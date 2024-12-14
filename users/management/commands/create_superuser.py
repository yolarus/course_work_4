from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Создание администратора
    """
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(
            email="admin@mail.ru",
            first_name="Руслан",
            last_name="Аляутдинов"
        )

        user.set_password("12345")
        user.is_staff = True
        user.is_superuser = True

        user.save()

        self.stdout.write(self.style.SUCCESS(f"Пользователь {user.email} с правами администратора успешно создан"))

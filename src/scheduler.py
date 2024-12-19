from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone

from config import main_logger
from users.models import User

from .utils import get_all_mailings_from_cache, send_mailing

user = User.objects.get(email="admin@mail.ru")
scheduler = BackgroundScheduler()


def auto_sending_mailing():
    """
    Автоматическая отправка всех рассылок со статусом 'Запущена' при достижении времени первой отправки.
    Перевод рассылки в завершенные после достижения времени окончания рассылки.
    """
    main_logger.info("Запущена автоматическая отправка рассылок")

    for mailing in get_all_mailings_from_cache():
        if mailing.time_of_the_first_sending <= timezone.now():
            mailing.status = "started"
            send_mailing(mailing.pk, user)

            main_logger.info(f"Отправлена рассылка {mailing}")
        elif mailing.time_of_the_completion <= timezone.now():
            mailing.status = "completed"

            main_logger.info(f"Завершена рассылка {mailing}")


def start_scheduler():
    """
    Запуск планировщика рассылок сообщений - сообщения рассылаются каждый день в 12:00 по Москве
    """
    print("Запущен scheduler")
    main_logger.info("Запущен планировщик задач scheduler")

    scheduler.add_job(auto_sending_mailing, "cron", hour="9", minute="00")
    scheduler.start()
    while True:
        sleep(30)

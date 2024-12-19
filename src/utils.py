from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from config import main_logger
from config.settings import CACHE_ENABLED
from mailings.models import AttemptMailing, Mailing, Recipient
from users.models import User


def check_photo(photo):
    """
    Проверка веса и формата загружаемой фотографии
    """
    max_size = 5 * 1024 ** 2
    if photo:
        if photo.size > max_size:
            main_logger.error("Загружаемое изображение превышает максимально допустимый размер")
            raise ValidationError("Размер изображения не должен превышать 5 Мб")

        elif photo.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            main_logger.error("Загружаемое изображение имеет неверный формат")
            raise ValidationError("Можно загрузить файлы только форматов JPEG, JPG, PNG")

        main_logger.info("Загружаемое изображение успешно прошло валидацию")
        return photo
    else:
        return False


def get_all_mailings_from_cache():
    """
    Получение списка всех рассылок из кеша / БД
    """
    if not CACHE_ENABLED:
        main_logger.info("Данные загружаются из БД")

        mailings = Mailing.objects.all()
    else:
        main_logger.info("Данные загружаются из кеша")

        mailings = cache.get("mailings")
        if not mailings:
            mailings = Mailing.objects.all()
            cache.set("mailings", mailings, 5 * 60)

            main_logger.info("Кеш пуст, данные перезаписаны на 5 минут")
    return mailings.order_by("id")


def get_all_recipients_from_cache():
    """
    Получение списка всех получателей рассылок из кеша / БД
    """
    if not CACHE_ENABLED:
        main_logger.info("Данные загружаются из БД")

        recipients = Recipient.objects.all()
    else:
        main_logger.info("Данные загружаются из кеша")

        recipients = cache.get("recipients")
        if not recipients:
            recipients = Recipient.objects.all()
            cache.set("recipients", recipients, 5 * 60)

            main_logger.info("Кеш пуст, данные перезаписаны на 5 минут")
    return recipients.order_by("last_name")


def get_all_users_from_cache():
    """
    Получение списка всех пользователей сервиса рассылок из кеша / БД
    """
    if not CACHE_ENABLED:
        main_logger.info("Данные загружаются из БД")

        users = User.objects.all()
    else:
        main_logger.info("Данные загружаются из кеша")

        users = cache.get("users")
        if not users:
            users = Recipient.objects.all()
            cache.set("users", users, 5 * 60)

            main_logger.info("Кеш пуст, данные перезаписаны на 5 минут")
    return users.order_by("id")


def get_recipients_list(mailing: Mailing | None = None):
    """
    Получение списка получателей указанной рассылки
    :param mailing: Рассылка сообщений Mailing
    :return: Список получателей рассылки Recipient
    """
    main_logger.info("Подготавливается список получателей")

    if mailing:
        recipients = mailing.recipients
    else:
        recipients = get_all_recipients_from_cache()
    return recipients.order_by("last_name")


def send_mailing(mailing_pk: int, user) -> str:
    """
    Отправка рассылки по ключу
    :param mailing_pk: Primary key модели Mailing
    :param user: Текущий пользователь
    :return: Ответ почтового сервера
    """
    mailing = get_object_or_404(Mailing, pk=mailing_pk)
    attempt = AttemptMailing.objects.create(mailing=mailing)
    try:
        main_logger.info(f"Выполняется попытка отправки {mailing}")

        send_mail(subject=mailing.message.subject,
                  message=mailing.message.body,
                  from_email=None,
                  recipient_list=[recipient.email for recipient in get_recipients_list(mailing)])
        mailing.status = "started"
        attempt.status = "successful"
        attempt.mail_server_response = "Рассылка успешно отправлена"

        main_logger.info("Рассылка успешно отправлена")
    except Exception as e:
        attempt.status = "unsuccessful"
        attempt.mail_server_response = e.args[1]

        main_logger.error(f"Попытка провалилась - {e.args[1]}")

    mailing.save()
    attempt.owner = user
    attempt.save()
    return attempt.mail_server_response


def get_statistic_to_index():
    """
    Сбор статистики для отображения на главной странице
    """
    main_logger.info("Подготовка статистики для страницы index.html")

    mailings = get_all_mailings_from_cache()
    mailings_count = mailings.count()
    started_mailings_count = mailings.filter(status="started").count()
    recipients = get_all_recipients_from_cache()
    recipients_count = recipients.count()
    result = {
        "mailings_count": mailings_count,
        "started_mailings_count": started_mailings_count,
        "recipients_count": recipients_count
    }
    return result


def get_personal_statistic(user):
    """
    Сбор статистики для отображения на странице статистики пользователя
    """
    main_logger.info("Подготовка статистики для страницы personal_statistic.html")

    mailings = Mailing.objects.filter(owner=user)
    result = {"mailings": []}
    for mailing in mailings:
        attempts = AttemptMailing.objects.filter(mailing=mailing)
        user_attempts = attempts.filter(owner=user)
        successful_attempts_count = attempts.filter(status="successful").count()
        recipients = get_recipients_list(mailing)
        result["mailings"].append((mailing, (f"было произведено {len(attempts)} попыток отправки, "
                                             f"{successful_attempts_count} из них успешны. "
                                             f"Лично вами было предпринято {len(user_attempts)}/{len(attempts)} "
                                             f"попыток. В рассылке состояло {len(recipients)} получателей. "
                                             f"Каждый из получателей на данных момент получил "
                                             f"{successful_attempts_count} сообщений.")))
    return result


def add_owner_to_instance(request, form):
    """
    Добавляет в поле owner модели текущего пользователя
    """
    instance = form.save()
    user = request.user
    instance.owner = user
    instance.save()

    main_logger.info(f"Владелец {instance} - {user}")


def get_queryset_for_owner(user, queryset):
    """
    Выборка списка объектов только для их владельцев
    """
    try:
        if user.is_superuser or user.groups.get(name="Managers"):
            return queryset.order_by("id")

        main_logger.info("Выдан доступ менеджера")
    except Group.DoesNotExist:

        main_logger.info("Выдан доступ владельца")
        return queryset.filter(owner=user).order_by("id")


def check_access_to_view(instance, user):
    """
    Проверка статуса владельца для просмотра объекта
    """
    try:
        if user == instance.owner or user.is_superuser or user.groups.get(name="Managers"):

            main_logger.info("Доступ разрешен")
            return instance

    except Group.DoesNotExist:

        main_logger.error("Доступ отклонен")
        raise PermissionDenied


def check_access_to_delete(instance, user):
    """
    Проверка статуса владельца для удаления объекта
    """
    if user == instance.owner or user.is_superuser:

        main_logger.info("Доступ разрешен")
        return instance

    main_logger.error("Доступ отклонен")
    raise PermissionDenied

from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from mailings.models import AttemptMailing, Mailing, Recipient


def check_photo(photo):
    """
    Проверка веса и формата загружаемой фотографии
    """
    max_size = 5 * 1024 ** 2
    if photo:
        if photo.size > max_size:
            raise ValidationError("Размер изображения не должен превышать 5 Мб")
        elif photo.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            raise ValidationError("Можно загрузить файлы только форматов JPEG, JPG, PNG")
        return photo
    else:
        return False


def get_recipients_list(mailing: Mailing | None = None):
    """
    Получение списка получателей указанной рассылки
    :param mailing: Рассылка сообщений Mailing
    :return: Список получателей рассылки Recipient
    """
    if mailing:
        recipients = mailing.recipients
    else:
        recipients = Recipient.objects.all()
    return recipients.order_by("last_name")


def send_mailing(mailing_pk: int) -> str:
    """
    Отправка рассылки по ключу
    :param mailing_pk: Primary key модели Mailing
    :return: Ответ почтового сервера
    """
    mailing = get_object_or_404(Mailing, pk=mailing_pk)
    attempt = AttemptMailing.objects.create(mailing=mailing)
    try:
        send_mail(subject=mailing.message.subject,
                  message=mailing.message.body,
                  from_email=None,
                  recipient_list=[recipient.email for recipient in get_recipients_list(mailing)])
        mailing.status = "started"
        attempt.status = "successful"
        attempt.mail_server_response = "Рассылка успешно отправлена"
    except Exception as e:
        mailing.status = "created"
        attempt.status = "unsuccessful"
        attempt.mail_server_response = e.args[1]
    mailing.save()
    attempt.save()
    return attempt.mail_server_response


def get_statistic_to_index():
    """
    Сбор статистики для отображения на главной странице
    """
    mailings = Mailing.objects.all()
    mailings_count = mailings.count()
    started_mailings_count = mailings.filter(status="started").count()
    recipients = Recipient.objects.all()
    recipients_count = recipients.count()
    result = {
        "mailings_count": mailings_count,
        "started_mailings_count": started_mailings_count,
        "recipients_count": recipients_count
    }
    return result

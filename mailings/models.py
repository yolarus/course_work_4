from django.db import models

from users.models import User

MAILING_STATUS = [
    ("completed", "Завершена"),
    ("created", "Создана"),
    ("started", "Запущена")
]

ATTEMPT_STATUS = [
    ("successful", "Успешно"),
    ("unsuccessful", "Неуспешно"),
]


# Create your models here.
class Recipient(models.Model):
    """
    Модель получателя рассылки
    """
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, verbose_name="Отчество", null=True, blank=True)
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Владелец", null=True, blank=True)

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"

    def __str__(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        else:
            return f"{self.last_name} {self.first_name}"


class Message(models.Model):
    """
    Модель сообщения рассылки
    """
    subject = models.CharField(max_length=150, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Владелец", null=True, blank=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    """
    Модель рассылки
    """
    time_of_the_first_sending = models.DateTimeField(verbose_name="Дата и время первой отправки")
    time_of_the_completion = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(max_length=25, choices=MAILING_STATUS, verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.PROTECT, verbose_name="Сообщение", related_name="mailings")
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели", related_name="mailings")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Владелец", null=True, blank=True)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("can_disable_mailing", "Can disable mailing")
        ]

    def __str__(self):
        return f"Рассылка №{self.pk}"


class AttemptMailing(models.Model):
    """
    Модель попытки рассылки сообщений для сбора статистики
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    status = models.CharField(max_length=15, choices=ATTEMPT_STATUS, verbose_name="Статус")
    mail_server_response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка", related_name="attempts")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Владелец", null=True, blank=True)

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"

    def __str__(self):
        return f"Попытка №{self.pk} от {self.created_at}"

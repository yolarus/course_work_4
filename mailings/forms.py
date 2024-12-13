from django.forms import ModelForm

from .models import Message, Mailing, AttemptMailing, Recipient


class MessageForm(ModelForm):
    """
    Форма для создания и редактирования сообщения рассылки
    """
    class Meta:
        model = Message
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        Стилизация формы при инициализации
        """
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields["subject"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Тема сообщения"
        })

        self.fields["body"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Текст сообщения",
            "rows": 8
        })

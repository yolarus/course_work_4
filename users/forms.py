from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm

from src.utils import check_photo

from .models import User


class UserRegisterForm(UserCreationForm):
    """
    Форма для регистрации пользователя в сервисе рассылок сообщений
    """
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        """
        Стилизация формы при инициализации
        """
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Email"
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите пароль"
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Повторите пароль"
        })


class LoginUserForm(AuthenticationForm):
    """
    Форма для входа пользователя в сервисе рассылок сообщений
    """
    def __init__(self, *args, **kwargs):
        """
        Стилизация формы при инициализации
        """
        super(LoginUserForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Email"
        })
        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите пароль"
        })


class UserProfileForm(ModelForm):
    """
    Форма для страницы информации о пользователе интернет-магазина
    """
    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "phone_number", "country", "avatar"]

    def __init__(self, *args, **kwargs):
        """
        Стилизация формы при инициализации
        """
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Email"
        })

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите ник"
        })

        self.fields["first_name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите имя"
        })

        self.fields["last_name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите фамилию"
        })

        self.fields["phone_number"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите телефон"
        })
        self.fields["country"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите страну"
        })

        self.fields["avatar"].widget.attrs.update({
            "class": "form-control",
        })

    def clean_avatar(self):
        """
        Проверка веса и формата загружаемой фотографии
        """
        avatar = self.files.get("avatar")
        check_photo(avatar)

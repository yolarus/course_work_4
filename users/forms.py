from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, UserCreationForm
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
    Форма для входа пользователя в сервис рассылок сообщений
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
    Форма для страницы информации о пользователе сервиса рассылок
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


class UserBlockForm(ModelForm):
    """
    Форма для страницы блокировки пользователя сервиса рассылок
    """
    class Meta:
        model = User
        fields = ["is_active"]

    def __init__(self, *args, **kwargs):
        """
        Стилизация формы при инициализации
        """
        super(UserBlockForm, self).__init__(*args, **kwargs)

        self.fields["is_active"].widget.attrs.update({
            "class": "form-check-input",
        })


class UserPasswordResetForm(PasswordResetForm):
    """
    Форма для отправки сообщения на почту для сброса пароля пользователя
    """
    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите email"
        })


class UserSetPasswordForm(SetPasswordForm):
    """
    Форма для ввода нового пароля пользователя
    """
    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super(UserSetPasswordForm, self).__init__(*args, **kwargs)

        self.fields["new_password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите новый пароль"
        })
        self.fields["new_password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Повторите новый пароль"
        })

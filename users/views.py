import secrets

from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER

from .forms import LoginUserForm, UserProfileForm, UserRegisterForm
from .models import User


# Create your views here.
class UserRegisterView(CreateView):
    """
    Класс-представление для регистрации пользователя
    """
    model = User
    template_name = "users/user_form.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """
        Отправка письма с верификацией после регистрации пользователя
        """
        user = form.save()
        user.is_active = False
        user.token = secrets.token_hex(16)
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{user.token}/"
        send_mail(subject="Подтверждение почты",
                  message=f"Добрый день! \nПерейдите по ссылке для подтверждения почты: \n{url}",
                  from_email=EMAIL_HOST_USER,
                  recipient_list=[user.email])
        return super().form_valid(form)


def email_verification(request, token):
    """
    Проверка верификации пользователя
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class LoginUserView(LoginView):
    """
    Класс-представление для страницы входа пользователя
    """
    form_class = LoginUserForm


class UserProfileView(UpdateView):
    """
    Класс-представление для обновления информации о пользователе
    """
    model = User
    template_name = "users/user_form.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("mailings:index")

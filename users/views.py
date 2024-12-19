import secrets

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetCompleteView, PasswordResetConfirmView,
                                       PasswordResetDoneView, PasswordResetView)
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from config import main_logger
from config.settings import EMAIL_HOST_USER
from src.utils import get_all_users_from_cache

from .forms import (LoginUserForm, UserBlockForm, UserPasswordResetForm, UserProfileForm, UserRegisterForm,
                    UserSetPasswordForm)
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
        try:
            send_mail(subject="Подтверждение почты",
                      message=f"Добрый день! \nПерейдите по ссылке для подтверждения почты: \n{url}",
                      from_email=EMAIL_HOST_USER,
                      recipient_list=[user.email])

            main_logger.info(f"Пользователь {user} успешно зарегистрировался")
        except Exception as e:

            main_logger.info(f"При регистрации пользователя {user} произошла ошибка - {e.args[1]}")
        return super().form_valid(form)


def email_verification(request, token):
    """
    Проверка верификации пользователя
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()

    main_logger.info(f"Пользователь {user} успешно прошел верификацию")
    return redirect(reverse("users:login"))


class LoginUserView(LoginView):
    """
    Класс-представление для страницы входа пользователя
    """
    form_class = LoginUserForm

    def get_success_url(self):
        main_logger.info(f"Пользователь {self.request.user} успешно авторизовался")
        return super().get_success_url()


class LogoutUserView(LogoutView):
    """
    Класс-представление для страницы выхода пользователя
    """
    next_page = "mailings:index"

    def get_success_url(self):
        main_logger.info("Пользователь вышел из системы")
        return super().get_success_url()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    Класс-представление для обновления информации о пользователе
    """
    model = User
    template_name = "users/user_form.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("mailings:index")

    def get_form_class(self):
        """
        Подбор соответствующей формы для редактирования пользователя
        """
        user = self.get_object()
        current_user = self.request.user

        main_logger.info(f"Пользователь {current_user} пытается отредактировать профиль пользователя {user}")

        if current_user == user or current_user.is_superuser:

            main_logger.info("Доступ пользователя разрешен")
            return UserProfileForm
        elif current_user.has_perm("users.can_block_user") and not user.is_superuser:

            main_logger.info("Доступ менеджера разрешен")
            return UserBlockForm

        main_logger.error("Доступ отклонен")
        raise PermissionDenied


@method_decorator(cache_page(5 * 60), name="dispatch")
class UserDetailView(LoginRequiredMixin, DetailView):
    """
    Класс-представление для страницы информации о пользователе
    """
    model = User
    template_name = "users/user_detail.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        """
        Проверка прав пользователя на просмотр страницы
        """
        user = super().get_object()
        current_user = self.request.user

        main_logger.info(f"Пользователь {current_user} пытается просмотреть профиль пользователя {user}")

        if current_user == user or current_user.has_perm("users.can_block_user"):

            main_logger.info("Доступ разрешен")
            return user

        main_logger.error("Доступ отклонен")
        raise PermissionDenied


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Класс-представление для страницы информации о всех пользователях
    """
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"
    paginate_by = 6
    permission_required = "users.can_block_user"

    def get_queryset(self):
        main_logger.info("Загрузка страницы user_list.html")
        return get_all_users_from_cache()


class UserPasswordResetView(PasswordResetView):
    """
    Класс-представление для отображения страницы с запросом на сброс пароля пользователя
    """
    template_name = "users/password_reset_form.html"
    form_class = UserPasswordResetForm
    subject_template_name = "users/password_reset_subject.txt"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")

    def get_success_url(self):
        email = self.request.POST.get("email")
        main_logger.info(f"Пользователь {email} хочет сбросить пароль")
        return super().get_success_url()


class UserPasswordResetDoneView(PasswordResetDoneView):
    """
    Класс-представление для отображения страницы после отправки сообщения для сброса пароля
    """
    template_name = "users/password_reset_done.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Класс-представление для отображения страницы для ввода нового пароля пользователя
    """
    template_name = "users/password_reset_confirm.html"
    form_class = UserSetPasswordForm
    success_url = reverse_lazy("users:password_reset_complete")

    def get_success_url(self):
        main_logger.info("Пользователь  подтверждает изменение пароля")
        return super().get_success_url()


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    """
    Класс-представление для завершения процесса сброса пароля
    """
    template_name = "users/password_reset_complete.html"

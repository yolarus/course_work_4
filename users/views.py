import secrets

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import (LoginView, PasswordResetView, PasswordResetCompleteView,
                                       PasswordResetDoneView, PasswordResetConfirmView)
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER

from .forms import LoginUserForm, UserBlockForm, UserProfileForm, UserRegisterForm, UserPasswordResetForm, UserSetPasswordForm
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
        if current_user == user or current_user.is_superuser:
            return UserProfileForm
        elif current_user.has_perm("users.can_block_user") and not user.is_superuser:
            return UserBlockForm
        raise PermissionDenied


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
        if current_user == user or current_user.has_perm("users.can_block_user"):
            return user
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
        return super().get_queryset().order_by("id")


class UserPasswordResetView(PasswordResetView):
    """
    Класс-представление для отображения страницы с запросом на сброс пароля пользователя
    """
    template_name = "users/password_reset_form.html"
    form_class = UserPasswordResetForm
    subject_template_name = "users/password_reset_subject.txt"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")


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


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    """
    Класс-представление для завершения процесса сброса пароля
    """
    template_name = "users/password_reset_complete.html"

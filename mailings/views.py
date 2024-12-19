from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from src.utils import (add_owner_to_instance, check_access_to_delete, check_access_to_view, get_personal_statistic,
                       get_queryset_for_owner, get_recipients_list, get_statistic_to_index, send_mailing, get_all_recipients_from_cache, get_all_mailings_from_cache)

from .forms import MailingForm, MailingManagerForm, MessageForm, RecipientForm
from .models import AttemptMailing, Mailing, Message, Recipient


# Create your views here.
class IndexView(TemplateView):
    template_name = "mailings/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_statistic_to_index())
        return context


class PersonalStatisticView(LoginRequiredMixin, TemplateView):
    template_name = "mailings/personal_statistic.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_personal_statistic(self.request.user))
        return context


class MessageCreateView(LoginRequiredMixin,CreateView):
    """
    Представление для страницы создания сообщения рассылки
    """
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        """
        Сохранение владельца сообщения для рассылки
        """
        add_owner_to_instance(self.request, form)
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для страницы редактирования сообщения рассылки
    """
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def get_form_class(self):
        """
        Подбор соответствующей формы для редактирования сообщения рассылки
        """
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MessageForm
        raise PermissionDenied

    def get_success_url(self):
        """
        Перенаправление на страницу сообщения рассылки
        """
        return reverse("mailings:message_detail", args=[self.kwargs.get("pk")])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для страницы подтверждения удаления сообщения рассылки
    """
    model = Message
    template_name = "mailings/message_confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")

    def get_object(self, queryset=None):
        """
        Проверка возможности пользователя удалять сообщения рассылки
        """
        return check_access_to_delete(super().get_object(queryset), self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для страницы сообщения рассылки
    """
    model = Message
    template_name = "mailings/message_detail.html"
    context_object_name = "message"

    def get_object(self, queryset=None):
        """
        Проверка возможности пользователя просматривать страницу сообщения рассылки
        """
        return check_access_to_view(super().get_object(queryset), self.request.user)


class MessageListView(LoginRequiredMixin, ListView):
    """
    Представление для страницы списка всех сообщений рассылки
    """
    model = Message
    template_name = "mailings/message_list.html"
    context_object_name = "messages"
    paginate_by = 3

    def get_queryset(self):
        queryset = get_queryset_for_owner(self.request.user, super().get_queryset())
        return queryset


class RecipientCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для страницы создания получателя рассылки
    """
    model = Recipient
    form_class = RecipientForm
    template_name = "mailings/recipient_form.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def form_valid(self, form):
        """
        Сохранение владельца получателя рассылки
        """
        add_owner_to_instance(self.request, form)
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для страницы редактирования получателя рассылки
    """
    model = Recipient
    form_class = RecipientForm
    template_name = "mailings/recipient_form.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def get_form_class(self):
        """
        Подбор соответствующей формы для редактирования получателя рассылки
        """
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return RecipientForm
        raise PermissionDenied

    def get_success_url(self):
        """
        Перенаправление на страницу получателя рассылки
        """
        return reverse("mailings:recipient_detail", args=[self.kwargs.get("pk")])


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для страницы подтверждения удаления получателя рассылки
    """
    model = Recipient
    template_name = "mailings/recipient_confirm_delete.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def get_object(self, queryset=None):
        """
        Проверка возможности пользователя удалять получателей рассылки
        """
        return check_access_to_delete(super().get_object(queryset), self.request.user)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для страницы получателя рассылки
    """
    model = Recipient
    template_name = "mailings/recipient_detail.html"
    context_object_name = "recipient"

    def get_object(self, queryset=None):
        """
        Проверка возможности пользователя просматривать страницу получателя рассылки
        """
        return check_access_to_view(super().get_object(queryset), self.request.user)


class RecipientListView(LoginRequiredMixin, ListView):
    """
    Представление для страницы списка всех получателей рассылки
    """
    model = Recipient
    template_name = "mailings/recipient_list.html"
    context_object_name = "recipients"
    paginate_by = 9

    def get_queryset(self):
        return get_queryset_for_owner(self.request.user, get_all_recipients_from_cache())


class MailingCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для страницы создания рассылки сообщений
    """
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def form_valid(self, form):
        """
        Сохранение владельца рассылки
        """
        add_owner_to_instance(self.request, form)
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для страницы редактирования рассылки сообщений
    """
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_form_class(self):
        """
        Подбор соответствующей формы для редактирования рассылки сообщений
        """
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingForm
        elif user.has_perm("mailings.can_disable_mailing"):
            return MailingManagerForm
        raise PermissionDenied

    def get_success_url(self):
        """
        Перенаправление на страницу рассылки сообщений
        """
        return reverse("mailings:mailing_detail", args=[self.kwargs.get("pk")])


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для страницы подтверждения удаления рассылки сообщений
    """
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_object(self, queryset=None):
        """
        Проверка возможности пользователя удалять рассылки сообщений
        """
        return check_access_to_delete(super().get_object(queryset), self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для страницы рассылки сообщений
    """
    model = Mailing
    template_name = "mailings/mailing_detail.html"
    context_object_name = "mailing"

    def get_object(self, queryset=None):
        """
        Проверка возможности пользователя просматривать страницу рассылки сообщений
        """
        return check_access_to_view(super().get_object(queryset), self.request.user)

    def get_context_data(self, **kwargs):
        """
        Добавление списка получателей рассылки в контекст
        """
        context = super().get_context_data()
        context["recipients"] = get_recipients_list(super().get_object())
        return context


class MailingListView(LoginRequiredMixin, ListView):
    """
    Представление для страницы списка всех рассылок сообщений
    """
    model = Mailing
    template_name = "mailings/mailing_list.html"
    context_object_name = "mailings"
    paginate_by = 6

    def get_queryset(self):
        return get_queryset_for_owner(self.request.user, get_all_mailings_from_cache())


class MailingSendView(LoginRequiredMixin, View):
    """
    Представление для отправки рассылки сообщений через интерфейс приложения
    """
    def get(self, request, pk):
        """
        Отправка рассылки через интерфейс приложения
        """
        send_mailing(pk, request.user)
        return redirect(reverse("mailings:index"))


class AttemptMailingListView(LoginRequiredMixin, ListView):
    """
    Представление для страницы списка всех попыток рассылок сообщений
    """
    model = AttemptMailing
    template_name = "mailings/attempt_mailing_list.html"
    context_object_name = "attempts"
    paginate_by = 6

    def get_queryset(self):
        return get_queryset_for_owner(self.request.user, super().get_queryset())

from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from src.utils import get_recipients_list, get_statistic_to_index, send_mailing

from .forms import MailingForm, MessageForm, RecipientForm
from .models import AttemptMailing, Mailing, Message, Recipient


# Create your views here.
class IndexView(TemplateView):
    template_name = "mailings/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_statistic_to_index())
        return context


class MessageCreateView(CreateView):
    """
    Представление для страницы создания сообщения рассылки
    """
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")


class MessageUpdateView(UpdateView):
    """
    Представление для страницы редактирования сообщения рассылки
    """
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def get_success_url(self):
        """
        Перенаправление на страницу сообщения рассылки
        """
        return reverse("mailings:message_detail", args=[self.kwargs.get("pk")])


class MessageDeleteView(DeleteView):
    """
    Представление для страницы подтверждения удаления сообщения рассылки
    """
    model = Message
    template_name = "mailings/message_confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")


class MessageDetailView(DetailView):
    """
    Представление для страницы сообщения рассылки
    """
    model = Message
    template_name = "mailings/message_detail.html"
    context_object_name = "message"


class MessageListView(ListView):
    """
    Представление для страницы списка всех сообщений рассылки
    """
    model = Message
    template_name = "mailings/message_list.html"
    context_object_name = "messages"
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("id")


class RecipientCreateView(CreateView):
    """
    Представление для страницы создания получателя рассылки
    """
    model = Recipient
    form_class = RecipientForm
    template_name = "mailings/recipient_form.html"
    success_url = reverse_lazy("mailings:recipient_list")


class RecipientUpdateView(UpdateView):
    """
    Представление для страницы редактирования получателя рассылки
    """
    model = Recipient
    form_class = RecipientForm
    template_name = "mailings/recipient_form.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def get_success_url(self):
        """
        Перенаправление на страницу получателя рассылки
        """
        return reverse("mailings:recipient_detail", args=[self.kwargs.get("pk")])


class RecipientDeleteView(DeleteView):
    """
    Представление для страницы подтверждения удаления получателя рассылки
    """
    model = Recipient
    template_name = "mailings/recipient_confirm_delete.html"
    success_url = reverse_lazy("mailings:recipient_list")


class RecipientDetailView(DetailView):
    """
    Представление для страницы получателя рассылки
    """
    model = Recipient
    template_name = "mailings/recipient_detail.html"
    context_object_name = "recipient"


class RecipientListView(ListView):
    """
    Представление для страницы списка всех получателей рассылки
    """
    model = Recipient
    template_name = "mailings/recipient_list.html"
    context_object_name = "recipients"
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("last_name")


class MailingCreateView(CreateView):
    """
    Представление для страницы создания рассылки сообщений
    """
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")


class MailingUpdateView(UpdateView):
    """
    Представление для страницы редактирования рассылки сообщений
    """
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_success_url(self):
        """
        Перенаправление на страницу рассылки сообщений
        """
        return reverse("mailings:mailing_detail", args=[self.kwargs.get("pk")])


class MailingDeleteView(DeleteView):
    """
    Представление для страницы подтверждения удаления рассылки сообщений
    """
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")


class MailingDetailView(DetailView):
    """
    Представление для страницы рассылки сообщений
    """
    model = Mailing
    template_name = "mailings/mailing_detail.html"
    context_object_name = "mailing"

    def get_context_data(self, **kwargs):
        """
        Добавление списка получателей рассылки в контекст
        """
        context = super().get_context_data()
        context["recipients"] = get_recipients_list(super().get_object())
        return context


class MailingListView(ListView):
    """
    Представление для страницы списка всех рассылок сообщений
    """
    model = Mailing
    template_name = "mailings/mailing_list.html"
    context_object_name = "mailings"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("id")


class MailingSendView(View):
    """
    Представление для отправки рассылки сообщений через интерфейс приложения
    """
    def get(self, request, pk):
        """
        Отправка рассылки через интерфейс приложения
        """
        send_mailing(pk)
        return redirect(reverse("mailings:index"))


class AttemptMailingListView(ListView):
    """
    Представление для страницы списка всех попыток рассылок сообщений
    """
    model = AttemptMailing
    template_name = "mailings/attempt_mailing_list.html"
    context_object_name = "attempts"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("id")

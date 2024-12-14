from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Message, Mailing, AttemptMailing, Recipient
from .forms import MessageForm, RecipientForm


# Create your views here.
class IndexView(TemplateView):
    template_name = "mailings/index.html"


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
    paginate_by = 6


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
    paginate_by = 6

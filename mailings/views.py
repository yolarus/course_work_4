from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Message, Mailing, AttemptMailing, Recipient
from .forms import MessageForm


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

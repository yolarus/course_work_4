from django.urls import path

from . import views
from .apps import MailingsConfig

app_name = MailingsConfig.name

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("personal_statistic/", views.PersonalStatisticView.as_view(), name="personal_statistic"),

    path("messages/", views.MessageListView.as_view(), name="message_list"),
    path("messages/detail/<int:pk>/", views.MessageDetailView.as_view(), name="message_detail"),
    path("messages/create/", views.MessageCreateView.as_view(), name="message_create"),
    path("messages/update/<int:pk>/", views.MessageUpdateView.as_view(), name="message_update"),
    path("messages/delete/<int:pk>/", views.MessageDeleteView.as_view(), name="message_delete"),

    path("recipients/", views.RecipientListView.as_view(), name="recipient_list"),
    path("recipients/detail/<int:pk>/", views.RecipientDetailView.as_view(), name="recipient_detail"),
    path("recipients/create/", views.RecipientCreateView.as_view(), name="recipient_create"),
    path("recipients/update/<int:pk>/", views.RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipients/delete/<int:pk>/", views.RecipientDeleteView.as_view(), name="recipient_delete"),

    path("mailings/", views.MailingListView.as_view(), name="mailing_list"),
    path("mailings/detail/<int:pk>/", views.MailingDetailView.as_view(), name="mailing_detail"),
    path("mailings/create/", views.MailingCreateView.as_view(), name="mailing_create"),
    path("mailings/update/<int:pk>/", views.MailingUpdateView.as_view(), name="mailing_update"),
    path("mailings/delete/<int:pk>/", views.MailingDeleteView.as_view(), name="mailing_delete"),
    path("mailings/send/<int:pk>/", views.MailingSendView.as_view(), name="mailing_send"),

    path("attempts/", views.AttemptMailingListView.as_view(), name="attempt_mailing_list"),
]

from django.urls import path

from newsletters.apps import NewslettersConfig
from newsletters.views import (MessageCreateView, MessageDeleteView, MessageDetailView, MessageListView,
                               MessageUpdateView, NewsletterRecipientCreateView, NewsletterRecipientDeleteView,
                               NewsletterRecipientDetailView, NewsletterRecipientListView,
                               NewsletterRecipientUpdateView)

app_name = NewslettersConfig.name

urlpatterns = [
    path("clients/", NewsletterRecipientListView.as_view(), name="clients_list"),
    path("clients/new/", NewsletterRecipientCreateView.as_view(), name="client_create"),
    path("clients/<int:pk>/update/", NewsletterRecipientUpdateView.as_view(), name="client_update"),
    path("clients/<int:pk>/", NewsletterRecipientDetailView.as_view(), name="client_detail"),
    path("clients/<int:pk>/delete/", NewsletterRecipientDeleteView.as_view(), name="client_delete"),
    path("messages/", MessageListView.as_view(), name="messages_list"),
    path("messages/new/", MessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("messages/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete")
]

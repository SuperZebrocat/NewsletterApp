from django.urls import path

from newsletters.apps import NewslettersConfig
from newsletters.views import NewsletterRecipientListView, NewsletterRecipientCreateView, NewsletterRecipientUpdateView, NewsletterRecipientDetailView, NewsletterRecipientDeleteView

app_name = NewslettersConfig.name

urlpatterns = [
    path('clients/', NewsletterRecipientListView.as_view(), name='clients_list'),
    path('clients/new/', NewsletterRecipientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/update/', NewsletterRecipientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/', NewsletterRecipientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/delete/', NewsletterRecipientDeleteView.as_view(), name='client_delete')
]
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from newsletters.forms import NewsletterRecipientForm, MessageForm
from newsletters.models import NewsletterRecipient, Message


class NewsletterRecipientListView(ListView):
    model = NewsletterRecipient
    template_name = "newsletters/clients_list.html"
    context_object_name = "clients"


class NewsletterRecipientCreateView(CreateView):
    model = NewsletterRecipient
    form_class = NewsletterRecipientForm
    template_name = "newsletters/client_form.html"
    success_url = reverse_lazy('newsletters:clients_list')


class NewsletterRecipientUpdateView(UpdateView):
    model = NewsletterRecipient
    form_class = NewsletterRecipientForm
    template_name = "newsletters/client_form.html"
    success_url = reverse_lazy('newsletters:clients_list')


class NewsletterRecipientDetailView(DetailView):
    model = NewsletterRecipient
    template_name = 'newsletters/client_detail.html'
    context_object_name = 'client'


class NewsletterRecipientDeleteView(DeleteView):
    model = NewsletterRecipient
    template_name = 'newsletters/client_confirm_delete.html'
    context_object_name = 'client'
    success_url = reverse_lazy('newsletters:clients_list')


class MessageListView(ListView):
    model = Message
    template_name = "newsletters/messages_list.html"
    context_object_name = "messages"


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletters/message_form.html"
    success_url = reverse_lazy('newsletters:messages_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletters/message_form.html"
    success_url = reverse_lazy('newsletters:messages_list')


class MessageDetailView(DetailView):
    model = Message
    template_name = 'newsletters/message_detail.html'
    context_object_name = 'message'


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'newsletters/message_confirm_delete.html'
    context_object_name = 'message'
    success_url = reverse_lazy('newsletters:messages_list')


# class Newsletter(models.Model):
#     pass
#
#
# class NewsletterAttempt(models.Model):
#     pass
#








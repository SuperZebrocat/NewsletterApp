from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from newsletters.forms import NewsletterRecipientForm
from newsletters.models import NewsletterRecipient


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

# class Message(models.Model):
#     subject = models.CharField(max_length=300, verbose_name="Тема письма", help_text="")
#     text = models.TextField()
#     pass
#
#
#
# class Newsletter(models.Model):
#     pass
#
#
# class NewsletterAttempt(models.Model):
#     pass
#








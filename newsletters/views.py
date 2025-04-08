from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from newsletters.forms import NewsletterRecipientForm, MessageForm, NewsletterForm
from newsletters.models import NewsletterRecipient, Message, Newsletter


class NewsletterRecipientListView(ListView):
    model = NewsletterRecipient
    template_name = "newsletters/clients_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        return NewsletterRecipient.objects.filter(owner=self.request.user)


class NewsletterRecipientCreateView(CreateView):
    model = NewsletterRecipient
    form_class = NewsletterRecipientForm
    template_name = "newsletters/client_form.html"
    success_url = reverse_lazy('newsletters:clients_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем текущего пользователя как владельца
        return super().form_valid(form)


class NewsletterRecipientUpdateView(UpdateView):
    model = NewsletterRecipient
    form_class = NewsletterRecipientForm
    template_name = "newsletters/client_form.html"
    success_url = reverse_lazy('newsletters:clients_list')


class NewsletterRecipientDetailView(DetailView):
    model = NewsletterRecipient
    template_name = 'newsletters/client_detail.html'
    context_object_name = 'client'

    def get_queryset(self):
        return NewsletterRecipient.objects.filter(owner=self.request.user)


class NewsletterRecipientDeleteView(DeleteView):
    model = NewsletterRecipient
    template_name = 'newsletters/client_confirm_delete.html'
    context_object_name = 'client'
    success_url = reverse_lazy('newsletters:clients_list')


class MessageListView(ListView):
    model = Message
    template_name = "newsletters/messages_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletters/message_form.html"
    success_url = reverse_lazy('newsletters:messages_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем текущего пользователя как владельца
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletters/message_form.html"
    success_url = reverse_lazy('newsletters:messages_list')


class MessageDetailView(DetailView):
    model = Message
    template_name = 'newsletters/message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'newsletters/message_confirm_delete.html'
    context_object_name = 'message'
    success_url = reverse_lazy('newsletters:messages_list')


class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = "newsletters/newsletter_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем текущего пользователя как владельца
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('newsletters:newsletter_detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаем текущего пользователя в форму
        return kwargs


class NewsletterListView(ListView):
    model = Newsletter
    template_name = "newsletters/newsletters_list.html"
    context_object_name = "newsletters"

    def get_queryset(self):
        return Newsletter.objects.filter(owner=self.request.user)


class NewsletterDetailView(DetailView):
    model = Newsletter
    template_name = 'newsletters/newsletter_detail.html'
    context_object_name = 'newsletter'

    def get_queryset(self):
        return Newsletter.objects.filter(owner=self.request.user)


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletters/newsletter_form.html'

    def get_success_url(self):
        return reverse_lazy('newsletters:newsletter_detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаем текущего пользователя в форму
        return kwargs


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    template_name = 'newsletters/newsletter_confirm_delete.html'
    context_object_name = 'newsletter'
    success_url = reverse_lazy('newsletters:newsletters_list')

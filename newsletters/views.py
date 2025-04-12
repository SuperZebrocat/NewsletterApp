from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from newsletters.forms import MessageForm, NewsletterForm, NewsletterManagerForm, NewsletterRecipientForm
from newsletters.models import Message, Newsletter, NewsletterRecipient

User = get_user_model()


class NewsletterRecipientListView(LoginRequiredMixin, ListView):  # список владельцам свои, менеджерам - всех
    model = NewsletterRecipient
    template_name = "newsletters/clients_list.html"

    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.groups.filter(name="managers").exists()
            or NewsletterRecipient.objects.filter(owner=request.user).exists()
        ):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def get_queryset(self):
        if self.request.user.groups.filter(name="managers").exists():
            return NewsletterRecipient.objects.all()
        return NewsletterRecipient.objects.filter(owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.groups.filter(name="managers").exists():
            context = super().get_context_data(**kwargs)
            users = User.objects.filter(is_staff=False).exclude(groups__name="managers")
            context["users"] = users

            clients_data = []
            for user in users:
                clients_list = list(NewsletterRecipient.objects.filter(owner=user))
                clients_data.append({"user": user, "clients_list": clients_list})
            context["clients_data"] = clients_data
            return context
        elif NewsletterRecipient.objects.filter(owner=self.request.user).exists():
            context = super().get_context_data(**kwargs)
            clients = list(NewsletterRecipient.objects.filter(owner=self.request.user))
            context["clients"] = clients
            return context


class NewsletterRecipientCreateView(LoginRequiredMixin, CreateView):  # создание всем зарег, кроме менеджеров
    """Представление для создания клиента - получателя рассылки."""

    model = NewsletterRecipient
    form_class = NewsletterRecipientForm
    template_name = "newsletters/client_form.html"
    success_url = reverse_lazy("newsletters:clients_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="managers").exists() and not request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем текущего пользователя как владельца
        return super().form_valid(form)


class NewsletterRecipientUpdateView(LoginRequiredMixin, UpdateView):  # редактирование только владельцам
    """Представление для редактирования клиента - получателя рассылки."""

    model = NewsletterRecipient
    form_class = NewsletterRecipientForm
    template_name = "newsletters/client_form.html"
    success_url = reverse_lazy("newsletters:clients_list")

    def dispatch(self, request, *args, **kwargs):
        client = self.get_object()
        if client.owner != self.request.user:
            raise PermissionDenied("Редактирование доступно только владельцу объекта")
        return super().dispatch(request, *args, **kwargs)


class NewsletterRecipientDetailView(LoginRequiredMixin, DetailView):  # владельцам свои, менеджерам - всех
    """Представление для просмотра деталей клиента - получателя рассылки"""

    model = NewsletterRecipient
    template_name = "newsletters/client_detail.html"
    context_object_name = "client"

    def get_queryset(self):
        if self.request.user.groups.filter(name="managers").exists():
            return NewsletterRecipient.objects.all()
        return NewsletterRecipient.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):  # редактировать профиль может только сам пользователь
        client = self.get_object()
        if not (request.user.groups.filter(name="managers").exists() or client.owner == self.request.user):
            raise PermissionDenied("У вас недостаточно прав для просмотра объекта")
        return super().dispatch(request, *args, **kwargs)


class NewsletterRecipientDeleteView(LoginRequiredMixin, DeleteView):  # удаление только владельцам
    """Представление для удаления клиента - получателя рассылки"""

    model = NewsletterRecipient
    template_name = "newsletters/client_confirm_delete.html"
    context_object_name = "client"
    success_url = reverse_lazy("newsletters:clients_list")

    def dispatch(self, request, *args, **kwargs):
        client = self.get_object()
        if client.owner != self.request.user:
            raise PermissionDenied("Удаление доступно только владельцу объекта")
        return super().dispatch(request, *args, **kwargs)


class MessageListView(LoginRequiredMixin, ListView):
    """Представление для списка писем пользователя"""

    model = Message
    template_name = "newsletters/messages_list.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="managers").exists() or Message.objects.filter(owner=request.user).exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def get_queryset(self):
        if self.request.user.groups.filter(name="managers").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.groups.filter(name="managers").exists():
            context = super().get_context_data(**kwargs)
            users = User.objects.filter(is_staff=False).exclude(groups__name="managers")
            context["users"] = users

            messages_data = []
            for user in users:
                messages_list = list(Message.objects.filter(owner=user))
                messages_data.append({"user": user, "messages_list": messages_list})
            context["messages_data"] = messages_data
            return context
        elif Message.objects.filter(owner=self.request.user).exists():
            context = super().get_context_data(**kwargs)
            messages = list(Message.objects.filter(owner=self.request.user))
            context["messages"] = messages
            return context


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Представление для деталей письма пользователя"""

    model = Message
    template_name = "newsletters/message_detail.html"
    context_object_name = "message"

    def get_queryset(self):
        if self.request.user.groups.filter(name="managers").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        message = self.get_object()
        if not (request.user.groups.filter(name="managers").exists() or message.owner == self.request.user):
            raise PermissionDenied("У вас недостаточно прав для просмотра объекта")
        return super().dispatch(request, *args, **kwargs)


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания письма"""

    model = Message
    form_class = MessageForm
    template_name = "newsletters/message_form.html"
    success_url = reverse_lazy("newsletters:messages_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="managers").exists() and not request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем текущего пользователя как владельца
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования письма"""

    model = Message
    form_class = MessageForm
    template_name = "newsletters/message_form.html"
    success_url = reverse_lazy("newsletters:messages_list")

    def dispatch(self, request, *args, **kwargs):
        message = self.get_object()
        if message.owner != request.user:
            raise PermissionDenied("Редактирование доступно только владельцу объекта")
        return super().dispatch(request, *args, **kwargs)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления письма"""

    model = Message
    template_name = "newsletters/message_confirm_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("newsletters:messages_list")

    def dispatch(self, request, *args, **kwargs):
        message = self.get_object()
        if message.owner != self.request.user:
            raise PermissionDenied("Удаление доступно только владельцу объекта")
        return super().dispatch(request, *args, **kwargs)


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания рассылки"""

    model = Newsletter
    form_class = NewsletterForm
    template_name = "newsletters/newsletter_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем текущего пользователя как владельца
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("newsletters:newsletter_detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # Передаем текущего пользователя в форму
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.groups.filter(name="managers").exists() or request.user.is_staff):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    template_name = "newsletters/newsletters_list.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="managers").exists() or Message.objects.filter(owner=request.user).exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def get_queryset(self):
        if self.request.user.groups.filter(name="managers").exists():
            return Newsletter.objects.all()
        return Newsletter.objects.filter(owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.groups.filter(name="managers").exists():
            context = super().get_context_data(**kwargs)
            users = User.objects.filter(is_staff=False).exclude(groups__name="managers")
            context["users"] = users

            newsletters_data = []
            for user in users:
                newsletters_list = list(Newsletter.objects.filter(owner=user))
                newsletters_data.append({"user": user, "newsletters_list": newsletters_list})
            context["newsletters_data"] = newsletters_data
            return context
        elif Newsletter.objects.filter(owner=self.request.user).exists():
            context = super().get_context_data(**kwargs)
            newsletters = list(Newsletter.objects.filter(owner=self.request.user))
            context["newsletters"] = newsletters
            return context


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = Newsletter
    template_name = "newsletters/newsletter_detail.html"
    context_object_name = "newsletter"

    def get_queryset(self):
        if self.request.user.groups.filter(name="managers").exists():
            return Newsletter.objects.all()
        return Newsletter.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        newsletter = self.get_object()
        if not (request.user.groups.filter(name="managers").exists() or newsletter.owner == self.request.user):
            raise PermissionDenied("У вас недостаточно прав для просмотра объекта")
        return super().dispatch(request, *args, **kwargs)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования рассылки"""

    model = Newsletter
    form_class = NewsletterForm
    template_name = "newsletters/newsletter_form.html"

    def get_success_url(self):
        if self.request.user.groups.filter(name="managers").exists():
            return reverse_lazy("newsletters:newsletters_list")
        return reverse_lazy("newsletters:newsletter_detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # Передаем текущего пользователя в форму
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        newsletter = self.get_object()
        if newsletter.owner != self.request.user and not self.request.user.groups.filter(name="managers").exists():
            raise PermissionDenied("Редактирование доступно только владельцу объекта")
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        newsletter = self.get_object()
        if newsletter.owner == self.request.user:
            return NewsletterForm
        elif self.request.user.groups.filter(name="managers").exists():
            return NewsletterManagerForm
        return super().get_form_class()


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления рассылки"""

    model = Newsletter
    template_name = "newsletters/newsletter_confirm_delete.html"
    context_object_name = "newsletter"
    success_url = reverse_lazy("newsletters:newsletters_list")

    def dispatch(self, request, *args, **kwargs):
        newsletter = self.get_object()
        if newsletter.owner != self.request.user:
            raise PermissionDenied("Удаление доступно только владельцу объекта")
        return super().dispatch(request, *args, **kwargs)

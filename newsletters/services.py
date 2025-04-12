from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from newsletters.models import Newsletter, NewsletterAttempting, NewsletterRecipient


class StartNewsletterView(LoginRequiredMixin, View):
    """Представление для отправки рассылки"""

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        newsletter = get_object_or_404(Newsletter, id=pk)
        if newsletter.owner != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        newsletter = get_object_or_404(Newsletter, id=pk)
        clients = newsletter.clients.all()
        subject = newsletter.message.subject
        text = newsletter.message.text

        for client in clients:
            try:
                send_mail(subject=subject, message=text, from_email=None, recipient_list=[client.email])
                NewsletterAttempting.objects.create(
                    status="successful", newsletter=newsletter, server_response="Рассылка успешно отправлена"
                )
                newsletter.status = "launched"
                newsletter.save()
                return HttpResponseRedirect(reverse("newsletters:newsletter_success", args=[pk]))
            except Exception as e:
                NewsletterAttempting.objects.create(
                    newsletter=newsletter,
                    status="failed",
                    server_response=str(e) if str(e) else "Неизвестная ошибка",
                )
                return HttpResponseRedirect(reverse("newsletters:newsletter_failed", args=[pk]))

    def get(self, request, pk):
        return HttpResponse("Используйте POST для отправки рассылки.")


class NewsletterConfirmStart(LoginRequiredMixin, View):
    """Представление для подтверждения отправки рассылки"""

    template_name = "newsletters/newsletter_confirm_start.html"

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        newsletter = get_object_or_404(Newsletter, id=pk)
        if newsletter.owner != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        newsletter = get_object_or_404(Newsletter, id=pk)

        if newsletter.status == "created" or newsletter.status == "launched":
            if newsletter.finish_sending not in [None, ""]:
                if newsletter.finish_sending >= timezone.now():
                    start_newsletter_view = StartNewsletterView.as_view()
                    return start_newsletter_view(request, pk=pk)  # Вызов метода post
                elif newsletter.finish_sending < timezone.now():
                    NewsletterAttempting.objects.create(
                        newsletter=newsletter,
                        status="failed",
                        server_response="Срок рассылки истек",
                    )
                    newsletter.status = "completed"
                    newsletter.save()
                    return HttpResponseRedirect(reverse("newsletters:newsletter_failed", args=[pk]))
            else:
                messages.error(request, "Укажите дату окончания рассылки")
                return HttpResponseRedirect(reverse("newsletters:newsletter_update", args=[pk]))
        elif newsletter.status == "completed":
            NewsletterAttempting.objects.create(
                newsletter=newsletter, status="failed", server_response="Срок рассылки истек."
            )
            return HttpResponseRedirect(reverse("newsletters:newsletter_failed", args=[pk]))

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        newsletter = get_object_or_404(Newsletter, id=pk)
        context = {
            "newsletter": newsletter,
        }
        return render(request, self.template_name, context)


class NewsletterStartSuccess(LoginRequiredMixin, TemplateView):
    """Представление для страницы успешной рассылки"""

    template_name = "newsletters/newsletter_success.html"

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        newsletter = get_object_or_404(Newsletter, id=pk)
        if newsletter.owner != request.user:
            raise PermissionDenied()
        last_attempt = newsletter.attempts.last()
        server_response = last_attempt.server_response if last_attempt else "Нет данных о попытке рассылки."
        context = self.get_context_data(newsletter=newsletter, server_response=server_response)
        return self.render_to_response(context)


class NewsletterStartFailed(LoginRequiredMixin, TemplateView):
    """Представление для страницы неуспешной рассылки"""

    template_name = "newsletters/newsletter_failed.html"

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        newsletter = get_object_or_404(Newsletter, id=pk)
        if newsletter.owner != request.user:
            raise PermissionDenied()
        last_attempt = newsletter.attempts.last()
        server_response = last_attempt.server_response if last_attempt else "Нет данных о попытке рассылки."
        context = self.get_context_data(newsletter=newsletter, server_response=server_response)
        return self.render_to_response(context)


class MainPageView(LoginRequiredMixin, TemplateView):
    """Представление для отображения главной страницы пользователю."""

    template_name = "newsletters/main_page.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.groups.filter(name="managers").exists():
            raise PermissionDenied("У вас нет прав доступа к этой странице.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Получаем количество рассылок пользователя
        newsletters_count = Newsletter.objects.filter(owner=user).count()
        newsletters_launched_count = Newsletter.objects.filter(owner=user, status="launched").count()
        # Получаем количество получателей всех рассылок пользователя
        clients_count = NewsletterRecipient.objects.filter(owner=user).count()
        # Добавляем данные в контекст
        context["newsletters_count"] = newsletters_count
        context["newsletters_launched_count"] = newsletters_launched_count
        context["clients_count"] = clients_count

        return context


class NewslettersLogs(LoginRequiredMixin, TemplateView):
    """Представление для страницы логов рассылок пользователя."""

    template_name = "newsletters/newsletters_logs.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.groups.filter(name="managers").exists():
            raise PermissionDenied("У вас нет прав доступа к этой странице.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        newsletters = Newsletter.objects.filter(owner=user)
        context["newsletters"] = newsletters

        newsletters_data = []

        for newsletter in newsletters:
            newsletter_attempts = NewsletterAttempting.objects.filter(newsletter=newsletter)
            if newsletter_attempts:
                newsletter_attempts_count = newsletter_attempts.count()
                successful_attempts_count = newsletter_attempts.filter(status="successful").count()
                failed_attempts_count = newsletter_attempts.filter(status="failed").count()

                newsletters_data.append(
                    {
                        "newsletter": newsletter,
                        "attempts_count": newsletter_attempts_count,
                        "successful_attempts_count": successful_attempts_count,
                        "failed_attempts_count": failed_attempts_count,
                    }
                )

        context["newsletters_data"] = newsletters_data

        attempts = NewsletterAttempting.objects.filter(newsletter__owner=user)
        all_successful_attempts_count = attempts.filter(status="successful").count()

        context["all_successful_attempts_count"] = all_successful_attempts_count

        return context

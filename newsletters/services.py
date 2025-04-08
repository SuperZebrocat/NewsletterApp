from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from newsletters.models import Newsletter, NewsletterAttempting


class StartNewsletterView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        newsletter = get_object_or_404(Newsletter, id=pk)
        clients = newsletter.clients.all()
        subject = newsletter.message.subject
        text = newsletter.message.text
        clients_email_list = [client.email for client in clients]

        try:
            send_mail(subject=subject, message=text, from_email=None, recipient_list=clients_email_list)
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
        newsletter = get_object_or_404(Newsletter, id=pk)
        if newsletter.owner != request.user:
            return HttpResponse("У вас нет прав на отправку этой рассылки.", status=403)
        return HttpResponse("Используйте POST для отправки рассылки.")


class NewsletterConfirmStart(View):
    template_name = "newsletters/newsletter_confirm_start.html"

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        newsletter = get_object_or_404(Newsletter, id=pk)

        if newsletter.status == "created":
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
        elif newsletter.status == "launched":
            NewsletterAttempting.objects.create(
                newsletter=newsletter,
                status="failed",
                server_response="Рассылка уже была отправлена. Вы не можете отправить её повторно.",
            )
            return HttpResponseRedirect(reverse("newsletters:newsletter_failed", args=[pk]))
        elif newsletter.status == "completed":
            NewsletterAttempting.objects.create(
                newsletter=newsletter, status="failed", server_response="Срок рассылки истек."
            )
            return HttpResponseRedirect(reverse("newsletters:newsletter_failed", args=[pk]))

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        newsletter = get_object_or_404(Newsletter, id=pk)

        # Проверка прав доступа
        if newsletter.owner != request.user:
            return HttpResponse("У вас нет прав на отправку этой рассылки.", status=403)

        # Отображение шаблона с вопросом
        context = {
            "newsletter": newsletter,
        }
        return render(request, self.template_name, context)


class NewsletterStartSuccess(TemplateView):
    template_name = "newsletters/newsletter_success.html"

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        newsletter = get_object_or_404(Newsletter, id=pk)
        last_attempt = newsletter.attempts.last()
        server_response = last_attempt.server_response if last_attempt else "Нет данных о попытке рассылки."
        context = self.get_context_data(newsletter=newsletter, server_response=server_response)
        return self.render_to_response(context)


class NewsletterStartFailed(TemplateView):
    template_name = "newsletters/newsletter_failed.html"

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        newsletter = get_object_or_404(Newsletter, id=pk)
        last_attempt = newsletter.attempts.last()
        server_response = last_attempt.server_response if last_attempt else "Нет данных о попытке рассылки."
        context = self.get_context_data(newsletter=newsletter, server_response=server_response)
        return self.render_to_response(context)

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from django.utils import timezone

from newsletters.models import Newsletter, NewsletterAttempting

User = get_user_model()


class Command(BaseCommand):
    help = 'Отправка рассылки по ID'

    def add_arguments(self, parser):
        parser.add_argument('newsletter_id', type=int, help='ID рассылки для отправки')
        parser.add_argument('email', type=str, help='Email пользователя')

    def handle(self, *args, **kwargs):
        newsletter_id = kwargs['newsletter_id']
        user_email = kwargs['email']

        newsletter = get_object_or_404(Newsletter, id=newsletter_id)
        user = get_object_or_404(User, email=user_email)

        if newsletter.owner != user:
            self.stderr.write(self.style.ERROR("У вас нет прав на отправку этой рассылки."))
            return

        if newsletter.finish_sending and newsletter.finish_sending < timezone.now():
            NewsletterAttempting.objects.create(
                newsletter=newsletter,
                status="failed",
                server_response="Срок рассылки истек.",
            )
            newsletter.status = "completed"
            newsletter.save()
            self.stderr.write(self.style.ERROR("Срок рассылки истек."))
            return

        clients = newsletter.clients.all()
        subject = newsletter.message.subject
        text = newsletter.message.text

        for client in clients:
            try:
                send_mail(subject=subject, message=text, from_email=None, recipient_list=[client.email])
                NewsletterAttempting.objects.create(
                    status="successful", newsletter=newsletter, server_response="Рассылка успешно отправлена"
                )
                self.stdout.write(self.style.SUCCESS(f"Рассылка успешно отправлена клиенту {client.email}"))
            except Exception as e:
                NewsletterAttempting.objects.create(
                    newsletter=newsletter,
                    status="failed",
                    server_response=str(e) if str(e) else "Неизвестная ошибка",
                )
                self.stderr.write(self.style.ERROR(f"Ошибка при отправке рассылки клиенту {client.email}: {e}"))

        newsletter.status = "launched"
        newsletter.save()

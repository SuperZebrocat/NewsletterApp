from django.db import models
from django.utils import timezone

from config import settings


class NewsletterRecipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", null=True, blank=True
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"


class Message(models.Model):
    subject = models.CharField(max_length=300, verbose_name="Тема письма")
    text = models.TextField(verbose_name="Текст письма")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", null=True, blank=True
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"


class Newsletter(models.Model):
    CREATED = "created"
    LAUNCHED = "launched"
    COMPLETED = "completed"

    STATUS_CHOICES = [
        (CREATED, "СОЗДАНА"),
        (LAUNCHED, "ЗАПУЩЕНА"),
        (COMPLETED, "ЗАВЕРШЕНА"),
    ]
    title = models.CharField(max_length=150, verbose_name="Название рассылки")
    start_sending = models.DateTimeField(
        verbose_name="Дата и время начала рассылки", default=timezone.now, blank=True, null=True
    )
    finish_sending = models.DateTimeField(
        verbose_name="Дата и время окончания рассылки",
        null=True,
        blank=True,
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created", verbose_name="Статус рассылки")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Письмо", related_name="newsletters")
    clients = models.ManyToManyField(
        NewsletterRecipient, related_name="newsletters", verbose_name="Получатели рассылки"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", null=True, blank=True
    )


class NewsletterAttempting(models.Model):
    SUCCESSFUL = "successful"
    FAILED = "failed"

    STATUS_CHOICES = [(SUCCESSFUL, "УСПЕШНО"), (FAILED, "НЕ УСПЕШНО")]

    timestamp = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="Дата и время попытки рассылки"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус попытки рассылки")
    server_answer = models.TextField()
    newsletter = models.ForeignKey(
        Newsletter, on_delete=models.CASCADE, related_name="newsletter", verbose_name="Рассылка"
    )

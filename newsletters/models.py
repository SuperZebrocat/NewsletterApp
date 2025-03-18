from django.db import models
from django.utils import timezone


class NewsletterRecipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"


class Message(models.Model):
    subject = models.CharField(max_length=300, verbose_name="Тема письма")
    text = models.TextField(verbose_name="Текст письма")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Newsletter(models.Model):
    CREATED = "created"
    LAUNCHED = "launched"
    COMPLETED = "completed"

    STATUS_CHOICES = [
        (CREATED, "Рассылка создана"),
        (LAUNCHED, "Рассылка запущена"),
        (COMPLETED, "Рассылка завершена"),
    ]
    title = models.CharField(max_length=150, verbose_name="Название рассылки")
    start_sending = models.DateTimeField(verbose_name="Дата и время начала рассылки", default=timezone.now)
    finish_sending = models.DateTimeField(
        verbose_name="Дата и время окончания рассылки",
        help_text="Укажите дату и время окончания рассылки",
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name='Статус рассылки'
    )
    comment = models.TextField(verbose_name="Комментарий")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='newsletters', verbose_name='Сообщение')
    client = models.ManyToManyField(NewsletterRecipient, related_name='newsletters', verbose_name='Получатели рассылки')

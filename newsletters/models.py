from django.db import models


class NewsletterRecipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Укажите Email получателя")
    full_name = models.CharField(max_length=255, verbose_name="ФИО", help_text="Укажите ФИО получателя")
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True, help_text="Укажите комментарий")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"

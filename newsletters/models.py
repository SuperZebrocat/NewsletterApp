from django.db import models


class NewsletterRecipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"

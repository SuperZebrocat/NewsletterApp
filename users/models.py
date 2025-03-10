from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(upload_to="users/avatars/", verbose_name="Аватар", blank=True, null=True,
                               help_text="Загрузите свой аватар")
    phone_number = models.CharField(max_length=35, verbose_name="Телефон", blank=True, null=True, help_text="Укажите номер телефона")
    country = CountryField(blank_label='выберите страну', blank=True, null=True, help_text="Выберите страну")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

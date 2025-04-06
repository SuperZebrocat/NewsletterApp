from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ImageField


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = ImageField(
        upload_to="avatars/", verbose_name="Аватар", blank=True, null=True, default="media/avatars/default_avatar.jpg"
    )
    phone_number = models.CharField(max_length=35, verbose_name="Телефон", blank=True, null=True)
    country = models.CharField(max_length=150, verbose_name="Страна", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

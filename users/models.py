from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ImageField


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = ImageField(
        upload_to="avatars/", verbose_name="Аватар", blank=True, null=True, default="avatars/default_avatar.jpg"
    )
    phone_number = models.CharField(max_length=35, verbose_name="Телефон", blank=True, null=True)
    country = models.CharField(max_length=150, verbose_name="Страна", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_deactivate_user", "Can deactivate user"),
            ("can_view_users_list", "Can view users list"),
        ]

    def __str__(self):
        return self.email

from django.contrib import admin

from users.forms import CustomUserCreationForm
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    list_filter = ('id', 'email')

from django.contrib import admin

from users.forms import UserCreationForm
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    list_filter = ('id', 'email')

    def save_model(self, request, obj, form, change):
        if not change:  # Если это создание нового пользователя
            password = form.cleaned_data.get('password')
            if password:
                obj.set_password(password)  # Хэшируем пароль
        super().save_model(request, obj, form, change)

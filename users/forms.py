from django import forms
from users.models import User


class UserCreationForm(forms.ModelForm):
    """Форма для создания пользователя через административную панель."""
    password = forms.CharField(widget=forms.PasswordInput)  # Поле для ввода пароля

    class Meta:
        model = User
        fields = ('email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Хэшируем пароль
        if commit:
            user.save()
        return user

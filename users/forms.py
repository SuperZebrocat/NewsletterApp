from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(max_length=254)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "phone_number", "country"]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["avatar"].widget = forms.FileInput(attrs={"class": "file-input", "style": "display: block;"})
        self.fields["avatar"].label = ""
        self.fields["phone_number"].widget.attrs.update({"class": "form-control", "placeholder": "Укажите телефон"})
        self.fields["country"].widget.attrs.update({"class": "form-control", "placeholder": "Укажите страну"})


class UserPasswordResetForm(PasswordResetForm):
    """Запрос на восстановление пароля"""
    email = forms.EmailField(label="", max_length=254, widget=forms.EmailInput(attrs={"placeholder": "Email"}))

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class UserSetNewPasswordForm(SetPasswordForm):
    """Изменение пароля пользователя после подтверждения"""
    def __init__(self, *args, **kwargs):
        """Обновление стилей формы"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})

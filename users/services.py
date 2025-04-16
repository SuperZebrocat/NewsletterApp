from django.contrib.auth import get_user_model, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView

from users.forms import CustomAuthenticationForm, UserPasswordResetForm, UserSetNewPasswordForm

User = get_user_model()


class CheckEmailView(TemplateView):
    template_name = "users/check_email.html"


class ActivateUserView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("users:register_success", email=user.email)
        else:
            return redirect("users:register_failed", email=user.email if user else "")


class EmailConfirmationSuccess(LoginView):
    template_name = "users/confirmation_success.html"
    form_class = CustomAuthenticationForm

    def get_success_url(self):
        return reverse_lazy("newsletters:clients_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        email = self.kwargs.get("email")
        context["message"] = f"Пользователь {email} успешно активирован. Вы можете войти в систему."
        return context


class EmailConfirmationFailed(LoginView):
    template_name = "users/confirmation_failed.html"
    form_class = CustomAuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        email = self.kwargs.get("email")

        if email:
            context["user_email"] = email  # Передаем email в контекст
            context["message"] = f"Ошибка при регистрации пользователя {email}."
        else:
            context["message"] = "Ошибка: адрес электронной почты не был передан."

        return context


class UserPasswordResetView(auth_views.PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = "users/password_reset_form.html"  # Укажите свой шаблон
    email_template_name = "users/password_reset_email.html"  # Укажите свой шаблон для email
    success_url = reverse_lazy("users:password_reset_done")  # URL для перенаправления после успешного сброса


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    email_template_name = "users/password_reset_email.html"
    subject_template_name = "users/password_reset_subject.txt"
    template_name = "users/password_reset_done.html"
    success_url = reverse_lazy("users:password_reset_complete")


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = UserSetNewPasswordForm
    template_name = "users/password_reset_confirm.html"  # Укажите свой шаблон
    success_url = reverse_lazy(
        "users:password_reset_complete"
    )  # URL для перенаправления после успешного подтверждения


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"  # Укажите свой шаблон

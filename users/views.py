from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from users.forms import CustomAuthenticationForm, CustomUserCreationForm, UserProfileForm

User = get_user_model()


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "users/login.html"


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:check_email")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy("users:user_activate", kwargs={"uidb64": uid, "token": token})
        current_site = Site.objects.get_current().domain
        send_mail(
            subject="Подтверждение регистрации",
            message=f"Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}",
            from_email="ekatesting@yandex.ru",
            recipient_list=[user.email],
        )
        return redirect("users:check_email")


class UserDetailView(DetailView):  # добавить права доступа
    model = User
    template_name = "users/profile_detail.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        email = self.kwargs.get("email")
        return get_object_or_404(User, email=email)


class UserUpdateView(UpdateView):  # добавить права доступа
    form_class = UserProfileForm
    template_name = "users/profile_update.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        email = self.kwargs.get("email")
        return get_object_or_404(User, email=email)

    def get_success_url(self):
        return reverse_lazy("users:profile_detail", kwargs={"email": self.object.email})

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

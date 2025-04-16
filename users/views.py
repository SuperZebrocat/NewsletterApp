from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from users.forms import CustomAuthenticationForm, CustomUserCreationForm, ManagerUserUpdateForm, UserProfileForm

User = get_user_model()


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "users/login.html"

    def get_success_url(self):
        user = self.request.user

        if user.groups.filter(name="managers").exists():
            return reverse("users:users_list")
        else:
            return super().get_success_url()  # URL из настроек для всех остальных


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


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/profile_detail.html"
    context_object_name = "user"

    def dispatch(self, request, *args, **kwargs):
        email = kwargs.get("email")
        user = get_object_or_404(User, email=email)

        if user != request.user:
            raise PermissionDenied("У вас нет прав доступа к этому профилю.")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        email = self.kwargs.get("email")
        return get_object_or_404(User, email=email)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = "users/profile_update.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        email = self.kwargs.get("email")
        return get_object_or_404(User, email=email)

    def get_success_url(self):
        user = self.get_object()
        if user == self.request.user:
            return reverse_lazy("users:profile_detail", kwargs={"email": user.email})
        elif self.request.user.has_perm("users.can_deactivate_user"):
            return reverse_lazy("users:users_list")
        else:
            return reverse_lazy("users:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()

        if not (request.user.groups.filter(name="managers").exists() or user == self.request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        user = self.get_object()

        if user == self.request.user:
            return UserProfileForm
        elif self.request.user.has_perm("users.can_deactivate_user"):
            return ManagerUserUpdateForm
        else:
            raise PermissionDenied()


@method_decorator(cache_page(60), name='dispatch')
class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = "users/users_list.html"
    permission_required = "users.can_view_users_list"

    def get_queryset(self):
        managers = Group.objects.get(name="managers")
        return User.objects.filter(is_staff=False).exclude(groups=managers)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        users = self.get_queryset()
        context["users"] = users

        return context

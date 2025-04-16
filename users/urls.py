from django.contrib.auth.views import LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.services import (
    CheckEmailView,
    ActivateUserView,
    EmailConfirmationSuccess,
    EmailConfirmationFailed,
    UserPasswordResetView,
    UserPasswordResetDoneView,
    UserPasswordResetConfirmView,
    UserPasswordResetCompleteView,
)

from users.views import RegisterView, CustomLoginView, UserDetailView, UserUpdateView, UserListView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("register//", CheckEmailView.as_view(), name="check_email"),
    path("activate/<uidb64>/<token>/", ActivateUserView.as_view(), name="user_activate"),
    path("register/success/<str:email>/", EmailConfirmationSuccess.as_view(), name="register_success"),
    path("register/failed/<str:email>/", EmailConfirmationFailed.as_view(), name="register_failed"),
    path("login/password_reset/", UserPasswordResetView.as_view(), name="password_reset"),
    path("login/password_reset/done/", UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("login/reset/<uidb64>/<token>/", UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("login/password_reset/complete/", UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="users:login"), name="logout"),
    path("profile/<str:email>/", UserDetailView.as_view(), name="profile_detail"),
    path("profile/<str:email>/update/", UserUpdateView.as_view(), name="profile_update"),
    path("users/", UserListView.as_view(), name="users_list"),
]

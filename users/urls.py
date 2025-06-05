from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.urls import path, reverse_lazy

from .apps import UsersConfig
from .views import ProfileView, RegisterView, verify_email

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "password/",
        PasswordChangeView.as_view(
            template_name="users/password.html",
            success_url=reverse_lazy("users:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password/done/",
        PasswordChangeDoneView.as_view(template_name="users/password_done.html"),
        name="password_change_done",
    ),
    path("verify/<uidb64>/<token>/", verify_email, name="verify-email"),
]

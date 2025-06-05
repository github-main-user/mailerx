from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from .apps import UsersConfig
from .views import ProfileView, RegisterView, verify_email

app_name = UsersConfig.name

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy("users:password_change_done")
        ),
        name="password_change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("verify/<uidb64>/<token>/", verify_email, name="verify_email"),
    # Step 1: Request reset
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy("users:password_reset_done")
        ),
        name="password_reset",
    ),
    # Step 2: Email sent notice
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    # Step 3: Link with token
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("users:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    # Step 4: Reset complete
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from .apps import UsersConfig
from .views import (
    ProfileView,
    RegisterView,
    ToggleUserBanView,
    UserListView,
    verify_email,
)

app_name = UsersConfig.name

urlpatterns = [
    # GENERAL
    path("", UserListView.as_view(), name="user_list"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("verify/<str:uidb64>/<str:token>/", verify_email, name="verify_email"),
    path(
        "block/<int:user_pk>/",
        ToggleUserBanView.as_view(),
        name="set_user_block_status",
    ),
    # PASSWORD CHANGE
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
    # PASSWORD RESET
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy("users:password_reset_done")
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("users:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

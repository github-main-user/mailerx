from typing import override

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView

from .forms import UserEditForm, UserRegisterForm
from .services import activate_user, send_verification_email

User = get_user_model()


def verify_email(request, uidb64, token):
    if activate_user(uidb64, token):
        messages.success(request, "Email verified successfully! Now, you can login.")
        return redirect("dashboard:home")

    messages.error(request, "Verification link is invalid or has expired.")
    return redirect("users:register")


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("dashboard:home")

    @override
    def form_valid(self, form):
        # user is not active by default, because of custom context manager
        user = form.save()
        send_verification_email(self.request, user)
        messages.warning(
            self.request, "Successful registration. Now you need to confirm you email."
        )
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = UserEditForm
    success_url = reverse_lazy("dashboard:home")

    @override
    def get_object(self, queryset=None):
        return self.request.user

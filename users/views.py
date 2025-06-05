from typing import override

from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView

from .forms import UserEditForm, UserRegisterForm

User = get_user_model()


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("dashboard:home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = UserEditForm
    success_url = reverse_lazy("dashboard:home")

    @override
    def get_object(self, queryset=None):
        return self.request.user

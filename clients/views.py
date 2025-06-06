from typing import override

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.mixins import (
    ManagerCreateForbiddenMixin,
    OwnerRequiredMixin,
    RoleFilteredListMixin,
)

from .forms import ClientForm
from .models import Client

User = get_user_model()


class ClientListView(LoginRequiredMixin, RoleFilteredListMixin, ListView):
    model = Client
    success_url = reverse_lazy("clients:client_list")


class ClientCreateView(LoginRequiredMixin, ManagerCreateForbiddenMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("clients:client_list")

    @override
    def form_valid(self, form):
        client = form.instance
        client.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("clients:client_list")


class ClientDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("clients:client_list")

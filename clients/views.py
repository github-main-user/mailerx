from typing import override

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView

from .forms import ClientForm
from .models import Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    @override
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm

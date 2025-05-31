from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView

from .forms import ClientForm
from .models import Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm

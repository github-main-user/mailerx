from typing import override

from django.views.generic import CreateView, ListView

from .forms import ClientForm
from .models import Client


class ClientListView(ListView):
    model = Client

    @override
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm

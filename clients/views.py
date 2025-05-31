from django.views.generic import ListView

from .models import Client


class ClientListView(ListView):
    model = Client

from django.views.generic import CreateView, ListView

from .forms import ClientForm
from .models import Client


class ClientListView(ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm

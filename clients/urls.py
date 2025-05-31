from django.urls import path

from .apps import ClientsConfig
from .views import ClientListView

app_name = ClientsConfig.name

urlpatterns = [
    path("", ClientListView.as_view(), name="client_list"),
]

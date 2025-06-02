from django.urls import path

from .apps import ClientsConfig
from .views import ClientCreateView, ClientDeleteView, ClientListView, ClientUpdateView

app_name = ClientsConfig.name

urlpatterns = [
    path("", ClientListView.as_view(), name="client_list"),
    path("create/", ClientCreateView.as_view(), name="client_create"),
    path("<int:pk>/update/", ClientUpdateView.as_view(), name="client_update"),
    path("<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
]

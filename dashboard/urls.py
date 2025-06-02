from django.urls import path

from .apps import DashboardConfig
from .views import HomeView

app_name = DashboardConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]

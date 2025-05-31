from django.urls import path

from .apps import MailingsConfig
from .views import HomeView

app_name = MailingsConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]

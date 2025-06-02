from django.urls import path

from .apps import MessagesConfig
from .views import (
    MessageCreateView,
    MessageDeleteView,
    MessageListView,
    MessageUpdateView,
)

app_name = MessagesConfig.name

urlpatterns = [
    path("", MessageListView.as_view(), name="message_list"),
    path("create/", MessageCreateView.as_view(), name="message_create"),
    path("<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
]

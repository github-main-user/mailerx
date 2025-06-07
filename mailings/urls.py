from django.urls import path

from .apps import MailingsConfig
from .views import (
    MailingCreateView,
    MailingDeleteView,
    MailingListView,
    MailingsLaunchView,
    MailingStartView,
    MailingToggleStatus,
    MailingUpdateView,
)

app_name = MailingsConfig.name

urlpatterns = [
    path("", MailingListView.as_view(), name="mailing_list"),
    path("create/", MailingCreateView.as_view(), name="mailing_create"),
    path("<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("<int:pk>/start/", MailingStartView.as_view(), name="mailing_start"),
    path(
        "<int:pk>/toggle-status/",
        MailingToggleStatus.as_view(),
        name="mailing_toggle_status",
    ),
    path("launch/", MailingsLaunchView.as_view(), name="mailing_launch"),
]

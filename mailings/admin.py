from django.contrib import admin

from .models import Mailing, MailingAttempt


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ["owner", "start_time", "end_time", "status", "message"]
    list_filter = ["owner", "start_time", "end_time", "status"]


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "status", "server_response", "mailing"]
    list_filter = ["timestamp", "status"]

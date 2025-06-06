from django.contrib import admin

from .models import Mailing, MailingAttempt


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ["owner", "start_time", "end_time", "status", "message", "is_active"]
    list_filter = ["owner", "start_time", "end_time", "status", "is_active"]


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "status", "server_response", "mailing"]
    list_filter = ["timestamp", "status"]

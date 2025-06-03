from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["owner", "subject", "body"]
    list_filter = ["owner"]
    search_fields = ["subject", "body"]

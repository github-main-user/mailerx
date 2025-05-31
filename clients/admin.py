from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["owner", "email", "full_name"]
    list_filter = ["owner", "email"]
    search_fields = ["full_name"]

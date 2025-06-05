from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "country",
        "is_active",
    ]
    list_filter = ["country", "is_active"]
    search_fields = ["first_name", "last_name"]

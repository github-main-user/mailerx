from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates "manager" group'

    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name="managers")

        permissions_codenames = [
            "can_view_all_users",
            "can_ban_users",
            "can_view_all_clients",
            "can_view_all_messages",
            "can_view_all_mailings",
            "can_disable_mailings",
        ]
        permissions = Permission.objects.filter(codename__in=permissions_codenames)
        group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS("Managers group created successfully"))

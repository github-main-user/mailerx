from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Creates test users, if DEBUG==True"

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write(self.style.ERROR(f"CAN'T CREATE USERS IN NOT DEBUG MODE"))
            return

        TEST_PASSWORD = "12345678"

        users_data = [
            {
                "email": "test@test.com",
                "first_name": "John",
                "last_name": "Piterson",
                "phone_number": "89259125329",
                "country": "USA",
                "role": User.UserRole.USER,
                "is_active": True,
            },
            {
                "email": "manager@manager.com",
                "role": User.UserRole.MANAGER,
                "is_active": True,
            },
            {
                "email": "admin@admin.com",
                "role": User.UserRole.USER,
                "is_active": True,
                "is_staff": True,
                "is_superuser": True,
            },
        ]

        for user_data in users_data:
            email = user_data.pop("email")
            user, created = User.objects.get_or_create(
                email=email,
                defaults=user_data,
            )
            if created:
                user.set_password(TEST_PASSWORD)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"User {user.email} is created"))
            else:
                self.stdout.write(
                    self.style.WARNING(f"User {user.email} already exists")
                )

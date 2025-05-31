from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Client(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clients")
    email = models.EmailField()
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "email"], name="unique_client_per_owner"
            )
        ]
        ordering = ("email",)
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.owner})"

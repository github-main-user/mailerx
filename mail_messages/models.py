from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    subject = models.CharField(max_length=255)
    body = models.TextField()

    class Meta:
        ordering = ("subject",)
        indexes = [
            models.Index(fields=["owner"]),
        ]

    def __str__(self):
        return self.subject

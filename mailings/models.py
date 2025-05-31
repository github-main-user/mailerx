from django.db import models


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    class Meta:
        ordering = ("subject",)

    def __str__(self):
        return self.subject

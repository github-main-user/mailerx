from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from clients.models import Client
from mail_messages.models import Message

User = get_user_model()


class Mailing(models.Model):
    class MailingStatus(models.TextChoices):
        CREATED = "CREATED", "Created"
        STARTED = "STARTED", "Started"
        FINISHED = "FINISHED", "Finished"

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mailings")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=8, choices=MailingStatus, default=MailingStatus.CREATED
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError({"end_time": "End time must be after start time."})

        # if mailing already started/finished - it can't exist before started
        if (
            self.status != self.MailingStatus.CREATED
            and self.start_time >= timezone.now()
        ):
            raise ValidationError(
                {"start_time": "Started/Finished Mailing can't exist before start_time"}
            )

    def __str__(self):
        return f'"{self.message}" ({self.status})'


class MailingAttempt(models.Model):
    class AttemptStatus(models.TextChoices):
        SUCCESS = "SUCCESS", "Success"
        FAIL = "FAIL", "Fail"

    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=8, choices=AttemptStatus)
    server_response = models.TextField()
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, related_name="attempts"
    )

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return f"{self.timestamp} ({self.status})"

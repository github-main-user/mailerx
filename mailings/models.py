from django.db import models

from clients.models import Client


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    class Meta:
        ordering = ("subject",)

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    class MailingStatus(models.TextChoices):
        CREATED = "CREATED", "Created"
        STARTED = "STARTED", "Started"
        FINISHED = "FINISHED", "Finished"

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=8, choices=MailingStatus, default=MailingStatus.CREATED
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)

    def __str__(self):
        return f'"{self.message}" ({self.status})'


class MailingAttempt(models.Model):
    class AttemptStatus(models.TextChoices):
        SUCCESS = "SUCCESS", "Success"
        FAIL = "FAIL", "Fail"

    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=8, choices=AttemptStatus)
    server_response = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return f"{self.timestamp} ({self.status})"

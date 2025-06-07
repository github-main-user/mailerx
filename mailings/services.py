from django.conf import settings
from django.core.mail import send_mail

from clients.models import Client

from .models import Mailing


def send_email_to_client(mailing: Mailing, client: Client) -> None:
    match mailing.status:
        case Mailing.MailingStatus.CREATED:
            print(f"Given mailing (#{mailing.pk}) is created, but not started.")
            return
        case Mailing.MailingStatus.FINISHED:
            print(f"Given mailing (#{mailing.pk}) is already finished.")
            return

    if not mailing.clients.filter(pk=client.pk).exists():
        print(
            f"Given client (#{client.pk}) is not in Mailing's (#{mailing.pk}) clients"
        )
        return

    send_mail(
        subject=mailing.message.subject,
        message=mailing.message.body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[client.email],
        fail_silently=False,
    )

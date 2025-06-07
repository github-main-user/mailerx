import logging

from django.conf import settings
from django.core.mail import send_mail

from clients.models import Client

from .models import Mailing

logger = logging.getLogger(__name__)


def send_email_to_client(mailing: Mailing, client: Client) -> None:
    """
    Sends email with message from given Mailing object to given Client.
    Sends it only if the mailing is STARTED and client is in the Mailing's list.
    """

    match mailing.status:
        case Mailing.MailingStatus.CREATED:
            logger.error("Given mailing (%s) is created, but not started.", mailing.pk)
            return
        case Mailing.MailingStatus.FINISHED:
            logger.error("Given mailing (%s) is already finished.", mailing.pk)
            return

    if not mailing.clients.filter(pk=client.pk).exists():
        logger.error(
            "Given client (%s) is not in Mailing's (%s) clients", client.pk, mailing.pk
        )
        return

    send_mail(
        subject=mailing.message.subject,
        message=mailing.message.body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[client.email],
        fail_silently=False,
    )

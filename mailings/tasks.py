import logging

from celery import shared_task
from django.utils import timezone

from .services import send_email_to_client

logger = logging.getLogger(__name__)


@shared_task
def send_email_to_client_task(mailing_id, client_id):
    from .models import Client, Mailing, MailingAttempt

    mailing = Mailing.objects.get(id=mailing_id)
    client = Client.objects.get(id=client_id)

    try:
        send_email_to_client(mailing, client)
        status = MailingAttempt.AttemptStatus.SUCCESS
        response = "Email sent successfully"
    except Exception as e:
        status = MailingAttempt.AttemptStatus.FAIL
        response = str(e)
        logger.error("Error during sending email to client %s", client.pk)
    else:
        logger.info("Email was successfully sent to client %s", client.pk)

    MailingAttempt.objects.create(
        mailing=mailing, client=client, status=status, server_response=response
    )


@shared_task
def send_started_mailings():
    from .models import Mailing, MailingAttempt

    mailings = Mailing.objects.filter(
        status=Mailing.MailingStatus.STARTED, is_active=True
    )
    logger.info("Got %s started mailings", mailings.count())
    for mailing in mailings:
        remaining_clients = mailing.clients.exclude(
            attempts__mailing=mailing,
            attempts__status=MailingAttempt.AttemptStatus.SUCCESS,
        )
        logger.info("Got %s remaining clients", remaining_clients.count())

        if not remaining_clients:
            mailing.status = Mailing.MailingStatus.FINISHED
            mailing.save()
            logger.info(
                "Mailing marked as finished since there are no remaining clients"
            )

        for client in remaining_clients:
            send_email_to_client_task.delay(mailing.id, client.id)


@shared_task
def finish_expired_tasks():
    from .models import Mailing

    now = timezone.now()
    expired_mailings = Mailing.objects.filter(
        status__in=[Mailing.MailingStatus.CREATED, Mailing.MailingStatus.STARTED],
        end_time__lte=now,
    )
    logger.info("Got %s expired task to finish", expired_mailings.count())
    expired_mailings.update(status=Mailing.MailingStatus.FINISHED)

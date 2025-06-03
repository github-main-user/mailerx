from django.conf import settings
from django.core.mail import send_mail

from .models import Mailing, MailingAttempt


def process_mailing(mailing: Mailing) -> None:
    """
    Processes a given mailing instance:
    - Sends the associated message to all clients.
    - Creates a MailingAttempt for each client.
    - Updates the mailing status accordingly.
    """

    match mailing.status:
        case Mailing.MailingStatus.CREATED:
            print(f"Given mailing (#{mailing.pk}) is created, but not started.")
            return
        case Mailing.MailingStatus.FINISHED:
            print(f"Given mailing (#{mailing.pk}) is already finished.")
            return

    try:
        send_mail(
            subject=mailing.message.subject,
            message=mailing.message.body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[client.email for client in mailing.clients.all()],
            fail_silently=False,
        )
        status = MailingAttempt.AttemptStatus.SUCCESS
        response = "Email sent successfully"

    except Exception as e:
        status = MailingAttempt.AttemptStatus.FAIL
        response = str(e)
    else:
        # finish the mailing only if there wasn't any exception
        mailing.status = Mailing.MailingStatus.FINISHED
        mailing.save()

    MailingAttempt.objects.create(
        mailing=mailing, status=status, server_response=response
    )

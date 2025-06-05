from django.views.generic import TemplateView

from clients.models import Client
from mail_messages.models import Message
from mailings.models import Mailing, MailingAttempt


class HomeView(TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            mailings = Mailing.objects.filter(owner=self.request.user)  # type: ignore
            mail_messages = Message.objects.filter(owner=self.request.user)  # type: ignore
            attempts = MailingAttempt.objects.filter(mailing__owner=self.request.user)  # type: ignore

            # clients **for current user**
            # since there is the (owner + email) unique constraint
            # each received client is unique
            clients = Client.objects.filter(owner=self.request.user)  # type: ignore

            context.update(
                {
                    "total_mailings": mailings.count(),
                    "active_mailings": mailings.filter(
                        status=Mailing.MailingStatus.STARTED
                    ).count(),
                    "unique_clients": clients.count(),
                    "total_messages": mail_messages.count(),
                    "successfull_attempts": attempts.filter(
                        status=MailingAttempt.AttemptStatus.SUCCESS
                    ).count(),
                    "failed_attempts": attempts.filter(
                        status=MailingAttempt.AttemptStatus.FAIL
                    ).count(),
                }
            )

        return context

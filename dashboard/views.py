from django.conf import settings
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from clients.models import Client
from mail_messages.models import Message
from mailings.models import Mailing, MailingAttempt


class HomeView(TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            clients = Client.objects.filter(owner=user)
            mail_messages = Message.objects.filter(owner=user)

            mailings = Mailing.objects.filter(owner=user).aggregate(
                total=Count("pk"),
                active=Count("pk", filter=Q(status=Mailing.MailingStatus.STARTED)),
            )

            attempts = MailingAttempt.objects.filter(mailing__owner=user).aggregate(
                success=Count(
                    "pk", filter=Q(status=MailingAttempt.AttemptStatus.SUCCESS)
                ),
                fail=Count("pk", filter=Q(status=MailingAttempt.AttemptStatus.FAIL)),
            )

            context.update(
                {
                    "total_mailings": mailings["total"],
                    "active_mailings": mailings["active"],
                    "total_clients": clients.count(),
                    "total_messages": mail_messages.count(),
                    "successfull_attempts": attempts["success"],
                    "failed_attempts": attempts["fail"],
                }
            )

        return context

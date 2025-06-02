from django.views.generic import TemplateView

from clients.models import Client
from mailings.models import Mailing


class HomeView(TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            mailings = Mailing.objects.filter(owner=self.request.user)  # type: ignore

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
                }
            )

        return context

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Count, Q
from django.views.generic import TemplateView

from clients.models import Client
from mail_messages.models import Message
from mailings.models import Mailing, MailingAttempt

User = get_user_model()


class HomeView(TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # managers can't create/update/delete so they don't need statistics
        if user.is_authenticated and user.role == User.UserRole.USER:
            cache_key = f"home_view_data_{user.pk}"
            cached_data = cache.get(cache_key)

            if not cached_data:
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
                    fail=Count(
                        "pk", filter=Q(status=MailingAttempt.AttemptStatus.FAIL)
                    ),
                )

                cached_data = {
                    "total_mailings": mailings["total"],
                    "active_mailings": mailings["active"],
                    "total_clients": clients.count(),
                    "total_messages": mail_messages.count(),
                    "successfull_attempts": attempts["success"],
                    "failed_attempts": attempts["fail"],
                }
                cache.set(cache_key, cached_data, settings.CACHE_QS_TIME_SEC)

            context.update(cached_data)

        return context

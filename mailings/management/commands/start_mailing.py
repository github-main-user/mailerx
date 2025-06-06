from django.core.management.base import BaseCommand

from mailings.models import Mailing
from mailings.services import process_mailing


class Command(BaseCommand):
    help = "Processes all started mailings."

    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(
            status=Mailing.MailingStatus.STARTED, is_active=True
        )
        for mailing in mailings:
            self.stdout.write(self.style.WARNING(f"Starting mailing #{mailing.pk}..."))
            process_mailing(mailing)
            self.stdout.write(self.style.SUCCESS(f"Mailing #{mailing.pk} completed."))

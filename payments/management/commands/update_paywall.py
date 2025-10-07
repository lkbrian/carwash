from django.core.management.base import BaseCommand

from payments.models import Paywall


class Command(BaseCommand):
    help = "Update or create Paywall record"

    def add_arguments(self, parser):
        parser.add_argument(
            "--status", type=str, help="Set payment status (e.g., pending, paid)"
        )
        parser.add_argument("--amount", type=int, help="Set payment amount")

    def handle(self, *args, **options):
        status = options.get("status")
        amount = options.get("amount")

        # Get or create the first Paywall record
        payment, created = Paywall.objects.get_or_create(id=1)

        if status:
            payment.status = status
        if amount:
            payment.amount = amount

        payment.save()

        action = "created" if created else "updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Paywall {action}: status={payment.status}, amount={payment.amount}"
            )
        )

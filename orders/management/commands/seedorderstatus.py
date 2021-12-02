from django.core.management.base import BaseCommand
from orders.models import Status


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Status.objects.all().delete()
        statuses = [
            "Pending",
            "Pre-Paid",
            "COD (Cash on Delivery)",
            "Failed",
            "Refunded",
            "Processing",
            "Delivered"

        ]
        for text in (statuses):
            Status.objects.create(text=text)
        self.stdout.write(self.style.SUCCESS(
            f"Seeding Complete!\nStatus Created: {len(statuses)}"))

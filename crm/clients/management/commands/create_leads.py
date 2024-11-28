from clients.factories import LeadFactory
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = (
        "Create random leads. Use it once. "
        "The other times there will be a uniqueness error"
    )

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Count of leads")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        self.stdout.write(f"Creating {count} random leads...")

        for num in range(count):
            lead = LeadFactory.create()
            self.stdout.write(
                f"Create #{num} advertising:\n"
                f"pk={lead.pk} first name={lead.first_name} "
                f"second name={lead.second_name} phone={lead.phone} "
                f"email={lead.email}\n"
                f"ads.pk={lead.ads.pk} "
                f"ads.name={lead.ads.name}\n"
                f"ads.product.pk={lead.ads.product.pk} "
                f"ads.product.name={lead.ads.product.name}"
            )
            lead.save()

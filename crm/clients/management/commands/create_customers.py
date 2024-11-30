from clients.factories import CustomerFactory
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = (
        "Create random customers."
    )

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Count of customers")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        self.stdout.write(f"Creating {count} random customers...")

        for num in range(count):
            customer = CustomerFactory.create()
            self.stdout.write(
                f"Create #{num} customer:\n"
                f"pk={customer.pk} first name={customer.lead.first_name} "
                f"last_name={customer.lead.last_name} phone={customer.lead.phone} "
                f"email={customer.lead.email}\n"
                f"contract.pk={customer.contract.pk}\n"
                f"contract.name={customer.contract.name}\n"
            )

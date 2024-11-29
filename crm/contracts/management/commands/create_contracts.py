from contracts.factories import ContractFactory
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = (
        "Create random contracts."
    )

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Count of contracts")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        self.stdout.write(f"Creating {count} random contracts...")

        for num in range(count):
            contract = ContractFactory.create()
            self.stdout.write(
                f"Create #{num} contract:\n"
                f"pk={contract.pk} name={contract.name}\n"
                f"product.pk={contract.product.pk} product.pk={contract.product.name}\n"
                f"doc.filename={contract.doc.name}\n"
                f"date={contract.date}\n"
                f"duration={contract.duration}\n"
                f"cost={contract.cost}\n"
            )

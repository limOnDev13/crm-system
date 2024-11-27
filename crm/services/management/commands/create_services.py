from django.core.management import BaseCommand

from services.factories import ServiceFactory


class Command(BaseCommand):
    help = "Create random services."

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Count of services")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        self.stdout.write(f"Creating {count} random products...")

        for num in range(count):
            service = ServiceFactory.create()
            self.stdout.write(
                f"Create #{num} service:\n"
                f"pk={service.pk} name={service.name} price={service.cost} description:\n{service.description}\n"
            )
            service.save()

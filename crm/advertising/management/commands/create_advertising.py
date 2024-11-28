from advertising.factories import AdvertisingFactory
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Create random advertising."

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Count of advertising")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        self.stdout.write(f"Creating {count} random advertising...")

        for num in range(count):
            advertising = AdvertisingFactory.create()
            self.stdout.write(
                f"Create #{num} advertising:\n"
                f"pk={advertising.pk} name={advertising.name} "
                f"channel={advertising.channel} budget={advertising.budget}\n"
                f"product.pk={advertising.product.pk}"
                f" product.name={advertising.product.name}"
            )
            advertising.save()

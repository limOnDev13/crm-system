import factory.faker
import factory.fuzzy
from services.factories import ServiceFactory

from .models import Advertising


class AdvertisingFactory(factory.django.DjangoModelFactory):
    """Advertising factory class."""

    class Meta:
        model = Advertising  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ("name", "channel", "budget", "product")

    name = factory.faker.Faker("word")
    channel = factory.faker.Faker("word")
    budget = factory.fuzzy.FuzzyFloat(0, 100, precision=4)
    product = factory.SubFactory(ServiceFactory)

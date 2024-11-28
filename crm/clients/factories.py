import factory.fuzzy
from advertising.factories import AdvertisingFactory

from .models import Lead


class LeadFactory(factory.django.DjangoModelFactory):
    """Lead factory."""

    class Meta:
        model = Lead
        django_get_or_create = ("first_name", "second_name", "phone", "email", "ads")

    first_name = factory.faker.Faker("first_name")
    second_name = factory.faker.Faker("last_name")
    phone = factory.Sequence(lambda n: f"+7 (999) 000 {n:04d}")
    email = factory.faker.Faker("email")
    ads = factory.SubFactory(AdvertisingFactory)

import factory.fuzzy

from .models import Lead
from advertising.factories import AdvertisingFactory


class LeadFactory(factory.django.DjangoModelFactory):
    """Lead factory."""

    class Meta:
        model = Lead
        django_get_or_create = (
            "first_name",
            "second_name",
            "phone",
            "email",
            "ads"
        )

    first_name = factory.faker.Faker("first_name")
    second_name = factory.faker.Faker("last_name")
    phone = factory.Sequence(lambda n: '+7 (999) 000 %04d' % n)
    email = factory.faker.Faker("email")
    ads = factory.SubFactory(AdvertisingFactory)

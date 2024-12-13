import random

import factory.fuzzy
from advertising.factories import AdvertisingFactory
from contracts.factories import ContractFactory

from .models import Customer, Lead


class LeadFactory(factory.django.DjangoModelFactory):
    """Lead factory."""

    class Meta:
        model = Lead
        django_get_or_create = ("first_name", "last_name", "phone", "email", "ads")

    first_name = factory.faker.Faker("first_name")
    last_name = factory.faker.Faker("last_name")
    phone = factory.LazyAttribute(
        lambda n: f"+7 (999) {random.randint(0, 999):03d} {random.randint(0, 9999):04d}"
    )
    email = factory.faker.Faker("email")
    ads = factory.SubFactory(AdvertisingFactory)


class CustomerFactory(factory.django.DjangoModelFactory):
    """Customer factory."""

    class Meta:
        model = Customer
        django_get_or_create = "lead", "contract"

    lead = factory.SubFactory(LeadFactory)
    contract = factory.SubFactory(ContractFactory)

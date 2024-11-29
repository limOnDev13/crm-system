import random
from datetime import timedelta
from typing import Optional
import os

import factory.fuzzy

from .models import Contract
from services.factories import ServiceFactory


def _create_empty_file(dir: Optional[str] = None, filename: str = "empty_file.txt") -> str:
    """Create empty file for factory."""
    if not dir:
        path = filename
    else:
        path = os.path.join(dir, filename)

    with open(path, encoding="UTF-8", mode="w"):
        pass

    return path


class ContractFactory(factory.django.DjangoModelFactory):
    """Contract factory."""

    class Meta:
        model = Contract
        django_get_or_create = ("name", "product", "doc", "date", "duration", "cost")

    name = factory.faker.Faker("word")
    product = factory.SubFactory(ServiceFactory)
    doc = factory.django.FileField(from_path=_create_empty_file())
    date = factory.faker.Faker("date_object")
    duration = timedelta(days=1)
    cost = factory.LazyAttribute(lambda x: round(random.uniform(0, 100), 2))

import os
import random
from datetime import datetime, timedelta
from typing import Optional

import factory.fuzzy
from services.factories import ServiceFactory

from .models import Contract


def _create_empty_file(
    file_dir: Optional[str] = None, filename: str = "empty_file.txt"
) -> str:
    """Create empty file for factory."""
    if not file_dir:
        path = filename
    else:
        path = os.path.join(file_dir, filename)

    with open(path, encoding="UTF-8", mode="w"):
        pass

    return path


class ContractFactory(factory.django.DjangoModelFactory):
    """Contract factory."""

    class Meta:
        model = Contract
        django_get_or_create = ("name", "product", "doc", "cost", "end_date")

    name = factory.faker.Faker("word")
    product = factory.SubFactory(ServiceFactory)
    doc = factory.django.FileField(from_path=_create_empty_file())
    cost = factory.LazyAttribute(lambda x: round(random.uniform(0, 100), 2))
    end_date = factory.LazyAttribute(lambda x: datetime.now() + timedelta(days=1))

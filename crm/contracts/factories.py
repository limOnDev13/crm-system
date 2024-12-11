import os
import random
from datetime import date, timedelta
from typing import Optional

import factory.fuzzy
from django.conf import settings
from services.factories import ServiceFactory

from .models import Contract


def _create_test_file(
    *,
    file_dir: Optional[str] = settings.BASE_DIR / "upload",
    filename: str = "test_file.txt"
) -> str:
    """Create empty file for factory."""
    if not file_dir:
        path = filename
    else:
        try:
            os.mkdir(file_dir)
        except FileExistsError:
            pass
        path = os.path.join(file_dir, filename)

    with open(path, encoding="UTF-8", mode="w") as file:
        file.write("Some data")

    return path


class ContractFactory(factory.django.DjangoModelFactory):
    """Contract factory."""

    class Meta:
        model = Contract
        django_get_or_create = ("name", "product", "doc", "cost", "end_date")

    name = factory.faker.Faker("word")
    product = factory.SubFactory(ServiceFactory)
    doc = factory.django.FileField(from_path=_create_test_file(file_dir="upload"))
    cost = factory.LazyAttribute(lambda x: round(random.uniform(0, 100), 2))
    end_date = factory.LazyAttribute(lambda x: date.today() + timedelta(days=1))

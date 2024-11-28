import factory.fuzzy

from .models import Service


class ServiceFactory(factory.django.DjangoModelFactory):
    """Service factory class."""

    class Meta:
        model = Service  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ("name", "description", "cost")

    name = factory.faker.Faker("word")
    description = factory.faker.Faker("text")
    cost = factory.fuzzy.FuzzyFloat(0, 100, precision=4)

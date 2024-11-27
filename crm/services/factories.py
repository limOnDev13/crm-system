import factory.faker
import factory.fuzzy
from services.models import Service


class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Service  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ("name", "description", "cost")

    name = factory.faker.Faker("word")
    description = factory.faker.Faker("text")
    cost = factory.fuzzy.FuzzyFloat(0, 100, precision=4)

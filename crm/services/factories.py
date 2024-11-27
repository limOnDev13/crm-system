import factory.fuzzy
import factory.faker

from services.models import Service


class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Service  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ("name", "description", "price")

    name = factory.faker.Faker("word")
    description = factory.faker.Faker("text")
    price = factory.fuzzy.FuzzyFloat(0, 100, precision=4)


if __name__ == "__main__":
    services = [ServiceFactory() for _ in range(10)]
    print(services)

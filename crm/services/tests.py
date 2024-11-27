from string import ascii_letters
import random

from django.test import TestCase
from django.urls import reverse
from factory.faker import Faker

from .models import Service


class ServicesListViewTest(TestCase):
    fixtures = [
        "services-fixtures.json",
    ]

    def test_services(self):
        response = self.client.get(reverse("services:services_list"))

        self.assertQuerySetEqual(
            qs=Service.objects.order_by("pk").all(),
            values=(s.pk for s in response.context["products"]),
            transform=lambda p: p.pk
        )


class ServicesDetailViewTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name="test service",
            description="test description",
            cost=random.uniform(0, 100)
        )

    def tearDown(self):
        self.service.delete()

    def test_get_service(self):
        response = self.client.get(reverse(
            "services:service_detail",
            kwargs={"pk": self.service.pk}
        ))

        self.assertEqual(response.status_code, 200)


class ServicesCreateViewTest(TestCase):
    def setUp(self):
        self.service_name = Faker("word")
        # Check that the object is being created in the test
        Service.objects.filter(name=self.service_name).delete()

    def test_create_service(self):
        response = self.client.post(
            reverse("services:service_create"),
            {
                "name": self.service_name,
                "description": Faker("description"),
                "cost": round(random.uniform(0, 100), 2),
            },
        )

        self.assertRedirects(response, reverse("services:services_list"))
        self.assertTrue(
            Service.objects.filter(name=self.service_name).exists()
        )

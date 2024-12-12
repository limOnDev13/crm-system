import random

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from factory.faker import Faker
from myauth.utils import create_group_marketers

from .factories import ServiceFactory
from .models import Service


class ServicesListViewTest(TestCase):
    """Test case class for testing ServicesListView."""

    fixtures = [
        "services-fixtures.json",
    ]

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="test", password="test")
        cls.user = User.objects.create_user(**cls.credentials)
        create_group_marketers()
        cls.group = Group.objects.get(name="marketers")
        cls.user.groups.add(cls.group)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.group.delete()

    def setUp(self):
        self.client.login(**self.credentials)

    def test_services(self):
        """Test getting list of services"""
        response = self.client.get(reverse("services:services_list"))

        self.assertQuerySetEqual(
            qs=Service.objects.order_by("pk").all(),
            values=sorted((s.pk for s in response.context["products"])),
            transform=lambda p: p.pk,
        )


class ServicesDetailViewTest(TestCase):
    """Test case class for testing ServicesDetailView."""

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="test", password="test")
        cls.user = User.objects.create_user(**cls.credentials)
        create_group_marketers()
        cls.group = Group.objects.get(name="marketers")
        cls.user.groups.add(cls.group)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.group.delete()

    def setUp(self):
        self.client.login(**self.credentials)
        self.service = ServiceFactory.create()

    def tearDown(self):
        self.service.delete()

    def test_get_service(self):
        """Test getting details about service."""
        response = self.client.get(
            reverse("services:service_detail", kwargs={"pk": self.service.pk})
        )

        self.assertEqual(response.status_code, 200)


class ServicesCreateViewTest(TestCase):
    """Test case class for testing ServicesCreateView."""

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="test", password="test")
        cls.user = User.objects.create_user(**cls.credentials)
        create_group_marketers()
        cls.group = Group.objects.get(name="marketers")
        cls.user.groups.add(cls.group)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.group.delete()

    def setUp(self):
        self.client.login(**self.credentials)
        self.service_name = Faker("word")
        # Check that the object is being created in the test
        Service.objects.filter(name=self.service_name).delete()
        self.service = None

    def tearDown(self):
        if self.service:
            self.service.delete()

    def test_create_service(self):
        """Test creating a new service."""
        response = self.client.post(
            reverse("services:service_create"),
            {
                "name": self.service_name,
                "description": Faker("description"),
                "cost": round(random.uniform(0, 100), 2),
            },
        )

        self.assertRedirects(response, reverse("services:services_list"))
        self.assertTrue(Service.objects.filter(name=self.service_name).exists())
        self.service = Service.objects.filter(name=self.service_name).first()


class ServiceUpdateViewTest(TestCase):
    """Test case class for testing ServiceUpdateView."""

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="test", password="test")
        cls.user = User.objects.create_user(**cls.credentials)
        create_group_marketers()
        cls.group = Group.objects.get(name="marketers")
        cls.user.groups.add(cls.group)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.group.delete()

    def setUp(self):
        self.client.login(**self.credentials)
        self.service = ServiceFactory.create()

    def tearDown(self):
        self.service.delete()

    def test_update_service(self):
        """Test updating the service."""
        updated_service = ServiceFactory()

        response = self.client.post(
            reverse(
                "services:service_edit",
                kwargs={"pk": self.service.pk},
            ),
            {
                "name": updated_service.name,
                "description": updated_service.description,
                "cost": updated_service.cost,
            },
        )

        # Check redirect
        self.assertRedirects(
            response,
            reverse(
                "services:service_detail",
                kwargs={"pk": self.service.pk},
            ),
        )
        # Check that the old primary key contains updated data
        service_ = Service.objects.filter(pk=self.service.pk).first()
        self.assertEqual(service_.name, updated_service.name)
        self.assertEqual(service_.description, updated_service.description)
        self.assertEqual(float(service_.cost), updated_service.cost)


class ServiceDeleteViewTest(TestCase):
    """Test case class for testing ServiceDeleteView."""

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="test", password="test")
        cls.user = User.objects.create_user(**cls.credentials)
        create_group_marketers()
        cls.group = Group.objects.get(name="marketers")
        cls.user.groups.add(cls.group)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.group.delete()

    def setUp(self):
        self.client.login(**self.credentials)
        self.service = ServiceFactory.create()

    def tearDown(self):
        self.service.delete()

    def test_delete_service(self):
        """Test deleting the service."""
        response = self.client.post(
            reverse(
                "services:service_delete",
                kwargs={"pk": self.service.pk},
            )
        )

        # Check redirect
        self.assertRedirects(response, reverse("services:services_list"))
        # Check that there is no data for the old primary key
        not_existing_service = Service.objects.filter(pk=self.service.pk).first()
        self.assertIsNone(not_existing_service)

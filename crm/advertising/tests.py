import random

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from factory.faker import Faker
from myauth.utils import create_group_marketers
from services.factories import ServiceFactory

from .factories import AdvertisingFactory
from .models import Advertising


class AdvertisingListViewTest(TestCase):
    """Test case class for testing AdvertisingListView."""

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

    fixtures = [
        "services-fixtures.json",
        "ads-fixtures.json",
    ]

    def test_get_list_advertising(self):
        """Test getting list of advertising"""
        response = self.client.get(reverse("advertising:ads_list"))

        self.assertQuerySetEqual(
            qs=Advertising.objects.order_by("pk").all(),
            values=(s.pk for s in response.context["ads"]),
            transform=lambda p: p.pk,
        )


class AdvertisingDetailViewTest(TestCase):
    """Test case class for testing AdvertisingDetailView."""

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
        self.ads = AdvertisingFactory.create()

    def tearDown(self):
        self.ads.delete()

    def test_get_details_about_ads(self):
        """Test getting details about advertising."""
        response = self.client.get(
            reverse("advertising:ads_detail", kwargs={"pk": self.ads.pk})
        )

        self.assertEqual(response.status_code, 200)


class AdsCreateViewTest(TestCase):
    """Test case class for testing AdvertisingCreateView."""

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
        self.ads_name = Faker("word")
        # Check that the object is being created in the test
        Advertising.objects.filter(name=self.ads_name).delete()
        self.product = ServiceFactory.create()

    def tearDown(self):
        self.product.delete()  # self.ads will be cascaded out

    def test_create_ads(self):
        """Test creating a new ads."""
        response = self.client.post(
            reverse("advertising:ads_create"),
            {
                "name": self.ads_name,
                "channel": Faker("word"),
                "budget": round(random.uniform(0, 100), 2),
                "product": self.product.id,
            },
        )

        self.assertRedirects(response, reverse("advertising:ads_list"))
        self.assertTrue(Advertising.objects.filter(name=self.ads_name).exists())


class AdsUpdateViewTest(TestCase):
    """Test case class for testing AdvertisingUpdateView."""

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
        self.ads = AdvertisingFactory.create()

    def tearDown(self):
        self.ads.delete()

    def test_update_ads(self):
        """Test updating the ads."""
        updated_ads = AdvertisingFactory()

        response = self.client.post(
            reverse(
                "advertising:ads_update",
                kwargs={"pk": self.ads.pk},
            ),
            {
                "name": updated_ads.name,
                "channel": updated_ads.channel,
                "budget": updated_ads.budget,
                "product": updated_ads.product.pk,
            },
        )

        # Check redirect
        self.assertRedirects(
            response,
            reverse(
                "advertising:ads_detail",
                kwargs={"pk": self.ads.pk},
            ),
        )
        # Check that the old primary key contains updated data
        ads_ = Advertising.objects.filter(pk=self.ads.pk).first()
        self.assertEqual(ads_.name, updated_ads.name)
        self.assertEqual(ads_.channel, updated_ads.channel)
        self.assertEqual(float(ads_.budget), updated_ads.budget)
        self.assertEqual(ads_.product.pk, updated_ads.product.pk)


class AdsDeleteViewTest(TestCase):
    """Test case class for testing AdvertisingDeleteView."""

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
        self.ads = AdvertisingFactory.create()

    def tearDown(self):
        self.ads.delete()

    def test_delete_ads(self):
        """Test deleting the ads."""
        response = self.client.post(
            reverse(
                "advertising:ads_delete",
                kwargs={"pk": self.ads.pk},
            )
        )

        # Check redirect
        self.assertRedirects(response, reverse("advertising:ads_list"))
        # Check that there is no data for the old primary key
        not_existing_ads = Advertising.objects.filter(pk=self.ads.pk).first()
        self.assertIsNone(not_existing_ads)

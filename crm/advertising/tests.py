import random

from django.test import TestCase
from django.urls import reverse
from factory.faker import Faker

from .factories import AdvertisingFactory
from .models import Advertising


class AdvertisingListViewTest(TestCase):
    """Test case class for testing AdvertisingListView."""

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

    def setUp(self):
        self.ads = AdvertisingFactory.create()

    def tearDown(self):
        self.ads.delete()

    def test_get_details_about_ads(self):
        """Test getting details about advertising."""
        response = self.client.get(
            reverse("advertising:ads_detail", kwargs={"pk": self.ads.pk})
        )

        self.assertEqual(response.status_code, 200)

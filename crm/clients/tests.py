import random

from django.test import TestCase
from django.urls import reverse
from factory.faker import Faker

from .factories import LeadFactory
from .models import Lead


class LeadsListViewTest(TestCase):
    """Test case class for testing LeadsListView."""

    fixtures = [
        "services-fixtures.json",
        "ads-fixtures.json",
        "leads-fixtures.json",
    ]

    def test_get_list_leads(self):
        """Test getting list of leads"""
        response = self.client.get(reverse("clients:leads_list"))

        self.assertQuerySetEqual(
            qs=Lead.objects.order_by("pk").all(),
            values=(s.pk for s in response.context["leads"]),
            transform=lambda p: p.pk,
        )


class LeadsDetailViewTest(TestCase):
    """Test case class for testing LeadDetailView."""

    def setUp(self):
        self.lead = LeadFactory.create()

    def tearDown(self):
        self.lead.delete()

    def test_get_details_about_lead(self):
        """Test getting details about the lead."""
        response = self.client.get(
            reverse("clients:leads_detail", kwargs={"pk": self.lead.pk})
        )

        self.assertEqual(response.status_code, 200)

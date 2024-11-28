from typing import Optional

from advertising.factories import AdvertisingFactory
from django.test import TestCase
from django.urls import reverse

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


class LeadsCreateViewTest(TestCase):
    """Test case class for testing LeadCreateView."""

    def setUp(self):
        self.lead_data = LeadFactory.build()
        self.ads = AdvertisingFactory.create()
        self.qs = Lead.objects.filter(
            first_name=self.lead_data.first_name,
            second_name=self.lead_data.second_name,
            phone=self.lead_data.phone,
            email=self.lead_data.email,
            ads=self.ads.pk,
        )

        # Check that the object is being created in the test
        self.qs.delete()

        self.lead: Optional[Lead] = None

    def tearDown(self):
        self.ads.delete()
        if self.lead:
            self.lead.delete()

    def test_create_lead(self):
        """Test creating a new lead."""
        response = self.client.post(
            reverse("clients:leads_create"),
            {
                "first_name": self.lead_data.first_name,
                "second_name": self.lead_data.second_name,
                "phone": self.lead_data.phone,
                "email": self.lead_data.email,
                "ads": self.ads.pk,
            },
        )

        self.assertRedirects(response, reverse("clients:leads_list"))
        self.assertTrue(self.qs.exists())
        self.lead = self.qs.first()

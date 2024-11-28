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


class LeadsUpdateViewTest(TestCase):
    """Test case class for testing LeadUpdateView."""

    def setUp(self):
        self.lead = LeadFactory.create()

    def tearDown(self):
        self.lead.delete()

    def test_update_lead(self):
        """Test updating the ads."""
        updated_lead = LeadFactory.build()
        updated_ads = AdvertisingFactory.create()

        response = self.client.post(
            reverse(
                "clients:leads_edit",
                kwargs={"pk": self.lead.pk},
            ),
            {
                "first_name": updated_lead.first_name,
                "second_name": updated_lead.second_name,
                "phone": updated_lead.phone,
                "email": updated_lead.email,
                "ads": updated_ads.pk,
            },
        )

        # Check redirect
        self.assertRedirects(
            response,
            reverse(
                "clients:leads_detail",
                kwargs={"pk": self.lead.pk},
            ),
        )
        # Check that the old primary key contains updated data
        lead_: Lead = Lead.objects.filter(pk=self.lead.pk).first()
        self.assertEqual(lead_.first_name, updated_lead.first_name)
        self.assertEqual(lead_.second_name, updated_lead.second_name)
        self.assertEqual(lead_.phone, updated_lead.phone)
        self.assertEqual(lead_.email, updated_lead.email)
        self.assertEqual(lead_.ads.pk, updated_ads.pk)


class LeadsDeleteViewTest(TestCase):
    """Test case class for testing LeadDeleteView."""

    def setUp(self):
        self.lead = LeadFactory.create()

    def tearDown(self):
        self.lead.delete()

    def test_delete_lead(self):
        """Test deleting the lead."""
        response = self.client.post(
            reverse(
                "clients:leads_delete",
                kwargs={"pk": self.lead.pk},
            )
        )

        # Check redirect
        self.assertRedirects(response, reverse("clients:leads_list"))
        # Check that there is no data for the old primary key
        not_existing_ads = Lead.objects.filter(pk=self.lead.pk).first()
        self.assertIsNone(not_existing_ads)

import random
from string import ascii_letters
from typing import Any, Dict, Optional

from advertising.factories import AdvertisingFactory
from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from myauth.utils import create_group_managers, create_group_operators

from .factories import LeadFactory
from .models import Customer, Lead


class LeadsListViewTest(TestCase):
    """Test case class for testing LeadsListView."""

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="test", password="test")
        cls.user = User.objects.create_user(**cls.credentials)
        create_group_managers()
        cls.group = Group.objects.get(name="managers")
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
        "leads-fixtures.json",
        "customers-fixtures.json",
        "contracts-fixtures.json",
    ]

    def test_get_list_leads(self):
        """Test getting list of leads"""
        response = self.client.get(reverse("clients:leads_list"))

        self.assertQuerySetEqual(
            qs=Lead.objects.order_by("pk").all(),
            values=(s.pk for s in response.context["leads"]),
            transform=lambda p: p.pk,
        )

    def test_all_leads_have_links_to_create_customer(self):
        """Test all leads have links to transfer to customers."""
        response = self.client.get(reverse("clients:leads_list"))

        leads = response.context["leads"]
        customers = Customer.objects.all()
        leads_are_customers = [customer.lead for customer in customers]
        leads_are_not_customers = [
            lead for lead in leads if lead not in leads_are_customers
        ]

        for lead_is_customer in leads_are_customers:
            self.assertNotContains(
                response, f"<a href=/customers/new/{lead_is_customer.pk}", html=True
            )

        for lead_is_not_customer in leads_are_not_customers:
            self.assertNotContains(
                response, f"<a href=/customers/new/{lead_is_not_customer.pk}", html=True
            )


class LeadsDetailViewTest(TestCase):
    """Test case class for testing LeadDetailView."""

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="test", password="test")
        cls.user = User.objects.create_user(**cls.credentials)
        create_group_operators()
        cls.group = Group.objects.get(name="operators")
        cls.user.groups.add(cls.group)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.group.delete()

    def setUp(self):
        self.client.login(**self.credentials)
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

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="test", password="test")
        cls.user = User.objects.create_user(**cls.credentials)
        create_group_operators()
        cls.group = Group.objects.get(name="operators")
        cls.user.groups.add(cls.group)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.group.delete()

    def setUp(self):
        self.client.login(**self.credentials)
        self.lead_data = LeadFactory.build()
        self.ads = AdvertisingFactory.create()
        self.qs = Lead.objects.filter(
            first_name=self.lead_data.first_name,
            last_name=self.lead_data.last_name,
            phone=self.lead_data.phone,
            email=self.lead_data.email,
            ads=self.ads.pk,
        )

        # Check that the object is being created in the test
        self.qs.delete()

        self.lead: Optional[Lead] = None
        self.request_kwargs: Dict[str, Any] = {
            "first_name": self.lead_data.first_name,
            "last_name": self.lead_data.last_name,
            "phone": self.lead_data.phone,
            "email": self.lead_data.email,
            "ads": self.ads.pk,
        }

    def tearDown(self):
        self.ads.delete()
        if self.lead:
            self.lead.delete()

    def test_create_lead(self):
        """Test creating a new lead."""
        response = self.client.post(
            reverse("clients:leads_create"),
            self.request_kwargs,
        )

        self.assertRedirects(response, reverse("clients:leads_list"))
        self.assertTrue(self.qs.exists())
        self.lead = self.qs.first()

    def test_creating_leads_with_identical_phones(self):
        """A negative test for creating leads with identical phones."""
        # Create first lead
        response = self.client.post(
            reverse("clients:leads_create"),
            self.request_kwargs,
        )

        self.assertRedirects(response, reverse("clients:leads_list"))
        self.assertTrue(self.qs.exists())
        self.lead = self.qs.first()

        # try creating a second lead with the same phone
        second_lead_data = LeadFactory.build()
        response = self.client.post(
            reverse("clients:leads_create"),
            {
                "first_name": second_lead_data.first_name,
                "last_name": second_lead_data.last_name,
                "phone": self.lead_data.phone,
                "email": second_lead_data.email,
                "ads": self.ads.pk,
            },
        )
        self.assertContains(
            response, "Lead with this Phone already exists.", html=False
        )

        # Check that there is no second entry in the database
        non_existing_lead = Lead.objects.filter(
            first_name=second_lead_data.first_name,
            last_name=second_lead_data.last_name,
            phone=self.lead_data.phone,
            email=second_lead_data.email,
            ads=self.ads.pk,
        ).first()
        self.assertIsNone(non_existing_lead)

    def test_creating_leads_with_identical_emails(self):
        """A negative test for creating leads with identical emails."""
        # Create first lead
        response = self.client.post(
            reverse("clients:leads_create"),
            self.request_kwargs,
        )

        self.assertRedirects(response, reverse("clients:leads_list"))
        self.assertTrue(self.qs.exists())
        self.lead = self.qs.first()
        if self.lead is None:
            self.fail("Self.lead is None...")
        else:
            # try creating a second lead with the same phone
            second_lead_data = LeadFactory.build()
            response = self.client.post(
                reverse("clients:leads_create"),
                {
                    "first_name": second_lead_data.first_name,
                    "last_name": second_lead_data.last_name,
                    "phone": second_lead_data.phone,
                    "email": self.lead.email,
                    "ads": self.ads.pk,
                },
            )
            self.assertContains(
                response, "Lead with this Email already exists.", html=False
            )

            # Check that there is no second entry in the database
            non_existing_lead = Lead.objects.filter(
                first_name=second_lead_data.first_name,
                last_name=second_lead_data.last_name,
                phone=second_lead_data.phone,
                email=self.lead_data.email,
                ads=self.ads.pk,
            ).first()
            self.assertIsNone(non_existing_lead)


class LeadsUpdateViewTest(TestCase):
    """Test case class for testing LeadUpdateView."""

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="test", password="test")
        cls.user = User.objects.create_user(**cls.credentials)
        create_group_operators()
        cls.group = Group.objects.get(name="operators")
        cls.user.groups.add(cls.group)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.group.delete()

    def setUp(self):
        self.client.login(**self.credentials)
        self.lead = LeadFactory.create()

    def tearDown(self):
        self.lead.delete()

    def test_update_lead(self):
        """Test updating the lead."""
        updated_lead = LeadFactory.build()
        updated_ads = AdvertisingFactory.create()

        response = self.client.post(
            reverse(
                "clients:leads_edit",
                kwargs={"pk": self.lead.pk},
            ),
            {
                "first_name": updated_lead.first_name,
                "last_name": updated_lead.last_name,
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
        self.assertEqual(lead_.last_name, updated_lead.last_name)
        self.assertEqual(lead_.phone, updated_lead.phone)
        self.assertEqual(lead_.email, updated_lead.email)
        self.assertEqual(lead_.ads.pk, updated_ads.pk)

    def test_updating_lead_with_invalid_phone(self):
        """Negative test for changing the phone field to an invalid phone."""
        updated_lead = LeadFactory.build()
        updated_ads = AdvertisingFactory.create()
        invalid_phone = "".join(random.choices(ascii_letters, k=random.randint(1, 15)))

        response = self.client.post(
            reverse(
                "clients:leads_edit",
                kwargs={"pk": self.lead.pk},
            ),
            {
                "first_name": updated_lead.first_name,
                "last_name": updated_lead.last_name,
                "phone": invalid_phone,
                "email": updated_lead.email,
                "ads": updated_ads.pk,
            },
        )
        form = response.context["form"]
        self.assertFormError(form, "phone", "Phone must have format +7 (999) 000 0000")

        # Check that self.lead has not changed in the database
        lead = Lead.objects.filter(pk=self.lead.pk).select_related("ads").first()
        self.assertTrue(lead.phone != invalid_phone)

    def test_changing_phone_field_to_existing_one(self):
        """Negative test for changing the phone field to an existing one."""
        second_lead = LeadFactory.create()
        updated_lead = LeadFactory.build()
        updated_ads = AdvertisingFactory.create()

        response = self.client.post(
            reverse(
                "clients:leads_edit",
                kwargs={"pk": self.lead.pk},
            ),
            {
                "first_name": updated_lead.first_name,
                "last_name": updated_lead.last_name,
                "phone": second_lead.phone,
                "email": updated_lead.email,
                "ads": updated_ads.pk,
            },
        )
        self.assertContains(
            response, "Lead with this Phone already exists.", html=False
        )

        # Check that self.lead has not changed in the database
        lead = Lead.objects.filter(pk=self.lead.pk).select_related("ads").first()
        self.assertTrue(lead.phone != second_lead.phone)

    def test_changing_email_field_to_existing_one(self):
        """Negative test for changing the email field to an existing one."""
        second_lead = LeadFactory.create()
        updated_lead = LeadFactory.build()
        updated_ads = AdvertisingFactory.create()

        response = self.client.post(
            reverse(
                "clients:leads_edit",
                kwargs={"pk": self.lead.pk},
            ),
            {
                "first_name": updated_lead.first_name,
                "last_name": updated_lead.last_name,
                "phone": updated_lead.phone,
                "email": second_lead.email,
                "ads": updated_ads.pk,
            },
        )
        self.assertContains(
            response, "Lead with this Email already exists.", html=False
        )

        # Check that self.lead has not changed in the database
        lead = Lead.objects.filter(pk=self.lead.pk).select_related("ads").first()
        self.assertTrue(lead.email != second_lead.email)


class LeadsDeleteViewTest(TestCase):
    """Test case class for testing LeadDeleteView."""

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="test", password="test")
        cls.user = User.objects.create_user(**cls.credentials)
        create_group_operators()
        cls.group = Group.objects.get(name="operators")
        cls.user.groups.add(cls.group)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.group.delete()

    def setUp(self):
        self.client.login(**self.credentials)
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

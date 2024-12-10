from typing import Optional, Dict, Any
from string import ascii_letters
import random
from copy import deepcopy
from datetime import timedelta

from advertising.factories import AdvertisingFactory
from contracts.factories import ContractFactory
from contracts.models import Contract
from django.test import TestCase
from django.urls import reverse

from services.factories import ServiceFactory
from .factories import LeadFactory, CustomerFactory
from .models import Lead, Customer
from .forms import NewCustomerForm


class LeadsListViewTest(TestCase):
    """Test case class for testing LeadsListView."""

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
        leads_are_not_customers = [lead for lead in leads if lead not in leads_are_customers]

        for lead_is_customer in leads_are_customers:
            self.assertNotContains(response, f"<a href=/customers/new/{lead_is_customer.pk}", html=True)

        for lead_is_not_customer in leads_are_not_customers:
            self.assertNotContains(response, f"<a href=/customers/new/{lead_is_not_customer.pk}", html=True)


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
        self.assertContains(response, "Lead with this Phone already exists.", html=False)

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
        self.assertContains(response, "Lead with this Email already exists.", html=False)

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
        self.assertContains(response, "Lead with this Phone already exists.", html=False)

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
        self.assertContains(response, "Lead with this Email already exists.", html=False)

        # Check that self.lead has not changed in the database
        lead = Lead.objects.filter(pk=self.lead.pk).select_related("ads").first()
        self.assertTrue(lead.email != second_lead.email)


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


class CustomerCreateViewTest(TestCase):
    """Test case class for testing CustomerCreateView."""

    def setUp(self):
        self.lead_data = LeadFactory.build()
        self.ads = AdvertisingFactory.create()
        self.product = ServiceFactory.create()
        self.contract_data = ContractFactory.build()
        self.lead_qs = Lead.objects.filter(
            phone=self.lead_data.phone,
            email=self.lead_data.email,
        )
        self.contract_qs = Contract.objects.filter(
            name=self.contract_data.name,
        )

        # Check that the object is being created in the test
        self.lead_qs.delete()
        self.contract_qs.delete()

        self.lead: Optional[Lead] = None
        self.contract: Optional[Contract] = None
        self.request_kwargs: Dict[str, Any] = {
            "first_name": self.lead_data.first_name,
            "last_name": self.lead_data.last_name,
            "phone": self.lead_data.phone,
            "email": self.lead_data.email,
            "ads": self.ads.pk,
            "name": self.contract_data.name,
            "product": self.product.pk,
            "doc": self.contract_data.doc,
            "end_date": self.contract_data.end_date,
            "cost": self.contract_data.cost,
        }

    def tearDown(self):
        if self.lead:
            self.lead.delete()
        if self.contract:
            self.contract.delete()
        # the customer is deleted cascadingly

    def test_create_customer(self):
        """Test creating a new customer."""
        response = self.client.post(
            reverse("clients:customers_new"),
            self.request_kwargs,
        )

        self.assertRedirects(response, reverse("clients:customers_list"))
        self.assertTrue(self.lead_qs.exists())
        self.assertTrue(self.contract_qs.exists())
        self.lead = self.lead_qs.first()
        self.contract = self.contract_qs.first()
        self.assertTrue(Customer.objects.filter(lead=self.lead, contract=self.contract).exists())

    def test_creating_customer_with_invalid_phone(self):
        """Negative test of creating a customer with an invalid phone."""
        kwargs = deepcopy(self.request_kwargs)
        kwargs["phone"] = "".join(random.choices(
            ascii_letters,
            k=random.randint(1, 10))
        )
        response = self.client.post(
            reverse("clients:customers_new"),
            kwargs,
        )
        form: NewCustomerForm = response.context["form"]
        self.assertFormError(form, "phone", "Phone must have format +7 (999) 000 0000")

    def test_creating_customer_with_identical_phones(self):
        """Negative test of creating a customer with an existing phone."""
        self.client.post(
            reverse("clients:customers_new"),
            self.request_kwargs,
        )
        self.lead = self.lead_qs.first()
        self.contract = self.contract_qs.first()

        # try creating second customer with identical phone
        second_lead_data = LeadFactory.build()
        second_contract_data = ContractFactory.build()
        response = self.client.post(
            reverse("clients:customers_new"),
            {
                "first_name": second_lead_data.first_name,
                "last_name": second_lead_data.last_name,
                "phone": self.lead_data.phone,
                "email": second_lead_data.email,
                "ads": self.ads.pk,
                "name": second_contract_data.name,
                "product": self.product.pk,
                "doc": second_contract_data.doc,
                "end_date": second_contract_data.end_date,
                "cost": second_contract_data.cost,
            },
        )
        form: NewCustomerForm = response.context["form"]
        self.assertFormError(form, "phone", "Phone already exists")

    def test_creating_customer_with_identical_emails(self):
        """Negative test of creating a customer with an existing email."""
        self.client.post(
            reverse("clients:customers_new"),
            self.request_kwargs,
        )
        self.lead = self.lead_qs.first()
        self.contract = self.contract_qs.first()

        # try creating second customer with identical email
        second_lead_data = LeadFactory.build()
        second_contract_data = ContractFactory.build()
        response = self.client.post(
            reverse("clients:customers_new"),
            {
                "first_name": second_lead_data.first_name,
                "last_name": second_lead_data.last_name,
                "phone": second_lead_data.phone,
                "email": self.lead_data.email,
                "ads": self.ads.pk,
                "name": second_contract_data.name,
                "product": self.product.pk,
                "doc": second_contract_data.doc,
                "end_date": second_contract_data.end_date,
                "cost": second_contract_data.cost,
            },
        )
        form: NewCustomerForm = response.context["form"]
        self.assertFormError(form, "email", "Email already exists")

    def test_creating_customer_with_identical_contract_names(self):
        """Negative test of creating a customer with an existing contract name."""
        self.client.post(
            reverse("clients:customers_new"),
            self.request_kwargs,
        )
        self.lead = self.lead_qs.first()
        self.contract = self.contract_qs.first()

        # try creating second customer with identical contract name
        second_lead_data = LeadFactory.build()
        second_contract_data = ContractFactory.build()
        response = self.client.post(
            reverse("clients:customers_new"),
            {
                "first_name": second_lead_data.first_name,
                "last_name": second_lead_data.last_name,
                "phone": second_lead_data.phone,
                "email": second_lead_data.email,
                "ads": self.ads.pk,
                "name": self.contract_data.name,
                "product": self.product.pk,
                "doc": second_contract_data.doc,
                "end_date": second_contract_data.end_date,
                "cost": second_contract_data.cost,
            },
        )
        form: NewCustomerForm = response.context["form"]
        self.assertFormError(form, "name", "Contract name already exists")

    def test_creating_customer_with_invalid_end_date(self):
        """Negative test of creating a customer with an invalid end date."""
        self.client.post(
            reverse("clients:customers_new"),
            self.request_kwargs,
        )
        self.lead = self.lead_qs.first()
        self.contract = self.contract_qs.first()

        # try creating second customer with identical contract name
        second_lead_data = LeadFactory.build()
        second_contract_data = ContractFactory.build()
        response = self.client.post(
            reverse("clients:customers_new"),
            {
                "first_name": second_lead_data.first_name,
                "last_name": second_lead_data.last_name,
                "phone": second_lead_data.phone,
                "email": second_lead_data.email,
                "ads": self.ads.pk,
                "name": second_contract_data.name,
                "product": self.product.pk,
                "doc": second_contract_data.doc,
                "end_date": self.contract.start_date - timedelta(days=random.randint(1, 10)),
                "cost": second_contract_data.cost,
            },
        )
        form: NewCustomerForm = response.context["form"]
        self.assertFormError(
            form,
            None,
            f"The end date must not be less than the start date ({self.contract.start_date})."
        )


class CustomersListViewTest(TestCase):
    """Test case class for testing CustomersListView."""

    fixtures = [
        "services-fixtures.json",
        "ads-fixtures.json",
        "leads-fixtures.json",
        "customers-fixtures.json",
        "contracts-fixtures.json",
    ]

    def test_get_list_customers(self):
        """Test getting list of customers"""
        response = self.client.get(reverse("clients:customers_list"))

        self.assertQuerySetEqual(
            qs=Customer.objects.order_by("pk").all(),
            values=(s.pk for s in response.context["customers"]),
            transform=lambda p: p.pk,
        )


class CustomerDeleteViewTest(TestCase):
    """Test case class for testing CustomerDeleteView."""

    def setUp(self):
        self.customer = CustomerFactory.create()

    def tearDown(self):
        self.customer.delete()

    def test_delete_customer(self):
        """Test deleting the customer."""
        response = self.client.post(
            reverse(
                "clients:customers_delete",
                kwargs={"pk": self.customer.pk},
            )
        )

        # Check redirect
        self.assertRedirects(response, reverse("clients:customers_list"))
        # Check that there is no data for the old primary key
        not_existing_ads = Customer.objects.filter(pk=self.customer.pk).first()
        self.assertIsNone(not_existing_ads)


class CustomerDetailViewTest(TestCase):
    """Test case class for testing CustomerDetailView."""

    def setUp(self):
        self.customer = CustomerFactory.create()

    def tearDown(self):
        self.customer.delete()

    def test_get_details_about_customer(self):
        """Test getting details about the customer."""
        response = self.client.get(
            reverse("clients:customers_detail", kwargs={"pk": self.customer.pk})
        )

        self.assertEqual(response.status_code, 200)

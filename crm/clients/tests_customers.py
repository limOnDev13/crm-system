import random
from copy import deepcopy
from datetime import date, timedelta
from string import ascii_letters
from typing import Any, Dict, Optional

from advertising.factories import AdvertisingFactory
from contracts.factories import ContractFactory
from contracts.models import Contract
from django.test import TestCase
from django.urls import reverse
from services.factories import ServiceFactory

from .factories import CustomerFactory, LeadFactory
from .forms import CustomerBaseForm, NewCustomerForm
from .models import Customer, Lead


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
        self.assertTrue(
            Customer.objects.filter(lead=self.lead, contract=self.contract).exists()
        )

    def test_creating_customer_with_invalid_phone(self):
        """Negative test of creating a customer with an invalid phone."""
        kwargs = deepcopy(self.request_kwargs)
        kwargs["phone"] = "".join(
            random.choices(ascii_letters, k=random.randint(1, 10))
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
        if self.contract is None:
            self.fail("self.contract is None...")
        else:
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
                    "end_date": self.contract.start_date
                    - timedelta(days=random.randint(1, 10)),
                    "cost": second_contract_data.cost,
                },
            )
            form: NewCustomerForm = response.context["form"]
            self.assertFormError(
                form,
                None,
                f"The end date must not be less than the start date"
                f" ({self.contract.start_date}).",
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


class UpdateCustomerTest(TestCase):
    """Test case class for testing update_customer."""

    def setUp(self):
        self.customer = CustomerFactory.create()

    def tearDown(self):
        self.customer.delete()

    def test_update_customer(self):
        """Test updating the customer."""
        previous_lead_pk = self.customer.lead.pk
        previous_contract_pk = self.customer.contract.pk
        updated_lead = LeadFactory.build()
        updated_contract = ContractFactory.build()
        ads = AdvertisingFactory.create()
        product = ServiceFactory.create()

        response = self.client.post(
            reverse(
                "clients:customers_edit",
                kwargs={"pk": self.customer.pk},
            ),
            {
                "first_name": updated_lead.first_name,
                "last_name": updated_lead.last_name,
                "phone": updated_lead.phone,
                "email": updated_lead.email,
                "ads": ads.pk,
                "name": updated_contract.name,
                "product": product.pk,
                "doc": updated_contract.doc,
                "end_date": updated_contract.end_date,
                "cost": updated_contract.cost,
            },
        )

        # Check redirect
        self.assertRedirects(
            response,
            reverse(
                "clients:customers_detail",
                kwargs={"pk": self.customer.pk},
            ),
        )
        # Check that the old primary key contains updated data
        customer_: Customer = (
            Customer.objects.filter(pk=self.customer.pk)
            .select_related("lead")
            .select_related("contract")
            .first()
        )
        self.assertEqual(customer_.lead.first_name, updated_lead.first_name)
        self.assertEqual(customer_.lead.last_name, updated_lead.last_name)
        self.assertEqual(customer_.lead.phone, updated_lead.phone)
        self.assertEqual(customer_.lead.email, updated_lead.email)
        self.assertEqual(customer_.lead.ads.pk, ads.pk)
        self.assertEqual(customer_.contract.name, updated_contract.name)
        self.assertEqual(customer_.contract.product.pk, product.pk)
        self.assertEqual(customer_.contract.end_date, updated_contract.end_date)
        self.assertEqual(float(customer_.contract.cost), updated_contract.cost)
        self.assertEqual(customer_.contract.pk, previous_contract_pk)
        self.assertEqual(customer_.lead.pk, previous_lead_pk)

    def test_updating_customer_changing_phone_field_to_existing_one(self):
        """Negative test for changing the phone field to an existing one."""
        second_lead = LeadFactory.create()
        updated_lead = LeadFactory.build()
        updated_contract = ContractFactory.build()
        ads = AdvertisingFactory.create()
        product = ServiceFactory.create()

        response = self.client.post(
            reverse(
                "clients:customers_edit",
                kwargs={"pk": self.customer.pk},
            ),
            {
                "first_name": updated_lead.first_name,
                "last_name": updated_lead.last_name,
                "phone": second_lead.phone,
                "email": updated_lead.email,
                "ads": ads.pk,
                "name": updated_contract.name,
                "product": product.pk,
                "doc": updated_contract.doc,
                "end_date": updated_contract.end_date,
                "cost": updated_contract.cost,
            },
        )
        self.assertContains(
            response, f"Key (phone)=({second_lead.phone}) already exists.", html=False
        )

        # Check that self.lead has not changed in the database
        customer = (
            Customer.objects.filter(pk=self.customer.pk).select_related("lead").first()
        )
        self.assertTrue(customer.lead.phone != second_lead.phone)

    def test_updating_customer_changing_email_field_to_existing_one(self):
        """Negative test for changing the email field to an existing one."""
        second_lead = LeadFactory.create()
        updated_lead = LeadFactory.build()
        updated_contract = ContractFactory.build()
        ads = AdvertisingFactory.create()
        product = ServiceFactory.create()

        response = self.client.post(
            reverse(
                "clients:customers_edit",
                kwargs={"pk": self.customer.pk},
            ),
            {
                "first_name": updated_lead.first_name,
                "last_name": updated_lead.last_name,
                "phone": updated_lead.phone,
                "email": second_lead.email,
                "ads": ads.pk,
                "name": updated_contract.name,
                "product": product.pk,
                "doc": updated_contract.doc,
                "end_date": updated_contract.end_date,
                "cost": updated_contract.cost,
            },
        )
        self.assertContains(
            response, f"Key (email)=({second_lead.email}) already exists.", html=False
        )

        # Check that self.lead has not changed in the database
        customer = (
            Customer.objects.filter(pk=self.customer.pk).select_related("lead").first()
        )
        self.assertTrue(customer.lead.email != second_lead.email)

    def test_updating_customer_changing_contract_name_field_to_existing_one(self):
        """Negative test for changing the name field to an existing one."""
        second_contract = ContractFactory.create()
        updated_lead = LeadFactory.build()
        updated_contract = ContractFactory.build()
        ads = AdvertisingFactory.create()
        product = ServiceFactory.create()

        response = self.client.post(
            reverse(
                "clients:customers_edit",
                kwargs={"pk": self.customer.pk},
            ),
            {
                "first_name": updated_lead.first_name,
                "last_name": updated_lead.last_name,
                "phone": updated_lead.phone,
                "email": updated_lead.email,
                "ads": ads.pk,
                "name": second_contract.name,
                "product": product.pk,
                "doc": updated_contract.doc,
                "end_date": updated_contract.end_date,
                "cost": updated_contract.cost,
            },
        )
        self.assertContains(
            response, f"Key (name)=({second_contract.name}) already exists.", html=False
        )

        # Check that self.lead has not changed in the database
        customer = (
            Customer.objects.filter(pk=self.customer.pk)
            .select_related("contract")
            .first()
        )
        self.assertTrue(customer.contract.name != second_contract.name)

    def test_updating_customer_entering_invalid_phone(self):
        """Negative test for changing the phone field to invalid format."""
        invalid_phone = "".join(random.choices(ascii_letters, k=random.randint(1, 10)))
        updated_lead = LeadFactory.build()
        updated_contract = ContractFactory.build()
        ads = AdvertisingFactory.create()
        product = ServiceFactory.create()

        response = self.client.post(
            reverse(
                "clients:customers_edit",
                kwargs={"pk": self.customer.pk},
            ),
            {
                "first_name": updated_lead.first_name,
                "last_name": updated_lead.last_name,
                "phone": invalid_phone,
                "email": updated_lead.email,
                "ads": ads.pk,
                "name": updated_contract.name,
                "product": product.pk,
                "doc": updated_contract.doc,
                "end_date": updated_contract.end_date,
                "cost": updated_contract.cost,
            },
        )
        self.assertContains(
            response, "Phone must have format +7 (999) 000 0000", html=False
        )

        # Check that self.lead has not changed in the database
        customer = (
            Customer.objects.filter(pk=self.customer.pk).select_related("lead").first()
        )
        self.assertTrue(customer.lead.phone != invalid_phone)

    def test_updating_customer_entering_invalid_end_date(self):
        """A negative test of the change of an active
        client when entering a past end date."""
        past_end_date: date = date.today() - timedelta(days=1)
        updated_lead = LeadFactory.build()
        updated_contract = ContractFactory.build()
        ads = AdvertisingFactory.create()
        product = ServiceFactory.create()

        response = self.client.post(
            reverse(
                "clients:customers_edit",
                kwargs={"pk": self.customer.pk},
            ),
            {
                "first_name": updated_lead.first_name,
                "last_name": updated_lead.last_name,
                "phone": updated_lead.phone,
                "email": updated_lead.email,
                "ads": ads.pk,
                "name": updated_contract.name,
                "product": product.pk,
                "doc": updated_contract.doc,
                "end_date": past_end_date.strftime("%Y-%m-%d"),
                "cost": updated_contract.cost,
            },
        )

        self.assertContains(
            response,
            f"The end date must not be less than the start date"
            f" ({self.customer.contract.start_date.strftime("%Y-%m-%d")}).",
            html=False,
        )

        # Check that self.lead has not changed in the database
        customer = (
            Customer.objects.filter(pk=self.customer.pk)
            .select_related("contract")
            .first()
        )
        self.assertTrue(customer.contract.end_date != past_end_date)


class CreateCustomerFromLeadTest(TestCase):
    """Test case class for testing view func create_customer_from_lead."""

    def setUp(self):
        self.lead = LeadFactory.create()
        self.product = ServiceFactory.create()
        self.contract_data = ContractFactory.build()
        self.contract_qs = Contract.objects.filter(
            name=self.contract_data.name,
        )
        self.customer_qs = Customer.objects.filter(lead=self.lead)

        # Check that the object is being created in the test
        self.customer_qs.delete()
        self.contract_qs.delete()

        self.contract: Optional[Contract] = None
        self.request_kwargs: Dict[str, Any] = {
            "first_name": self.lead.first_name,
            "last_name": self.lead.last_name,
            "phone": self.lead.phone,
            "email": self.lead.email,
            "ads": self.lead.ads.pk,
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

    def test_create_customer_from_lead(self):
        """Test creating a new customer from the lead."""
        response = self.client.post(
            reverse(
                "clients:customers_from_lead",
                kwargs={"lead_pk": self.lead.pk},
            ),
            self.request_kwargs,
        )

        self.assertRedirects(response, reverse("clients:customers_list"))
        self.assertTrue(self.customer_qs.exists())
        self.assertTrue(self.contract_qs.exists())
        self.contract = self.contract_qs.first()
        self.assertTrue(
            Customer.objects.filter(lead=self.lead, contract=self.contract).exists()
        )

    def test_create_customer_from_lead_with_updating_lead(self):
        """
        Test for creating an active user from
        a lead with changes to the lead data.
        """
        updated_lead = LeadFactory.build()
        new_ads = AdvertisingFactory.create()
        kwargs = deepcopy(self.request_kwargs)
        kwargs.update(
            {
                "first_name": updated_lead.first_name,
                "last_name": updated_lead.last_name,
                "email": updated_lead.email,
                "phone": updated_lead.phone,
                "ads": new_ads.pk,
            }
        )
        response = self.client.post(
            reverse(
                "clients:customers_from_lead",
                kwargs={"lead_pk": self.lead.pk},
            ),
            kwargs,
        )

        self.assertRedirects(response, reverse("clients:customers_list"))
        self.assertTrue(self.customer_qs.exists())
        self.assertTrue(self.contract_qs.exists())
        self.contract = self.contract_qs.first()
        self.assertTrue(
            Customer.objects.filter(lead=self.lead, contract=self.contract).exists()
        )
        self.lead = Lead.objects.filter(pk=self.lead.pk).first()
        if self.lead is None:
            self.fail("self.lead is None...")
        else:
            self.assertEqual(self.lead.first_name, updated_lead.first_name)
            self.assertEqual(self.lead.last_name, updated_lead.last_name)
            self.assertEqual(self.lead.email, updated_lead.email)
            self.assertEqual(self.lead.phone, updated_lead.phone)
            self.assertEqual(self.lead.ads.pk, new_ads.pk)

    def test_creating_customer_from_lead_with_invalid_phone(self):
        """Negative test of creating a customer with an invalid phone."""
        kwargs = deepcopy(self.request_kwargs)
        kwargs["phone"] = "".join(
            random.choices(ascii_letters, k=random.randint(1, 10))
        )
        response = self.client.post(
            reverse(
                "clients:customers_from_lead",
                kwargs={"lead_pk": self.lead.pk},
            ),
            kwargs,
        )
        form: CustomerBaseForm = response.context["form"]
        self.assertFormError(form, "phone", "Phone must have format +7 (999) 000 0000")
        not_existing_contact = self.contract_qs.first()
        self.assertIsNone(not_existing_contact)

    def test_creating_customer_from_lead_with_identical_phones(self):
        """Negative test of creating a customer with an existing phone."""
        second_lead: Lead = LeadFactory.create()

        response = self.client.post(
            reverse(
                "clients:customers_from_lead",
                kwargs={"lead_pk": self.lead.pk},
            ),
            {
                "first_name": self.lead.first_name,
                "last_name": self.lead.last_name,
                "phone": second_lead.phone,
                "email": self.lead.email,
                "ads": self.lead.ads.pk,
                "name": self.contract_data.name,
                "product": self.product.pk,
                "doc": self.contract_data.doc,
                "end_date": self.contract_data.end_date,
                "cost": self.contract_data.cost,
            },
        )
        self.assertContains(
            response, f"Key (phone)=({second_lead.phone}) already exists."
        )
        second_lead.delete()

        not_existing_contract = self.contract_qs.first()
        self.assertIsNone(not_existing_contract)
        not_existing_customer = self.customer_qs.first()
        self.assertIsNone(not_existing_customer)

    def test_creating_customer_from_lead_with_identical_emails(self):
        """Negative test of creating a customer with an existing email."""
        second_lead: Lead = LeadFactory.create()

        response = self.client.post(
            reverse(
                "clients:customers_from_lead",
                kwargs={"lead_pk": self.lead.pk},
            ),
            {
                "first_name": self.lead.first_name,
                "last_name": self.lead.last_name,
                "phone": self.lead.phone,
                "email": second_lead.email,
                "ads": self.lead.ads.pk,
                "name": self.contract_data.name,
                "product": self.product.pk,
                "doc": self.contract_data.doc,
                "end_date": self.contract_data.end_date,
                "cost": self.contract_data.cost,
            },
        )
        self.assertContains(
            response, f"Key (email)=({second_lead.email}) already exists."
        )
        second_lead.delete()

        not_existing_contract = self.contract_qs.first()
        self.assertIsNone(not_existing_contract)
        not_existing_customer = self.customer_qs.first()
        self.assertIsNone(not_existing_customer)

    def test_creating_customer_from_lead_with_identical_contract_names(self):
        """Negative test of creating a customer with an existing contract name."""
        second_contract: Contract = ContractFactory.create()

        response = self.client.post(
            reverse(
                "clients:customers_from_lead",
                kwargs={"lead_pk": self.lead.pk},
            ),
            {
                "first_name": self.lead.first_name,
                "last_name": self.lead.last_name,
                "phone": self.lead.phone,
                "email": self.lead.email,
                "ads": self.lead.ads.pk,
                "name": second_contract.name,
                "product": self.product.pk,
                "doc": self.contract_data.doc,
                "end_date": self.contract_data.end_date,
                "cost": self.contract_data.cost,
            },
        )
        self.assertContains(response, "Contract name already exists")
        second_contract.delete()

        not_existing_contract = self.contract_qs.first()
        self.assertIsNone(not_existing_contract)
        not_existing_customer = self.customer_qs.first()
        self.assertIsNone(not_existing_customer)

    def test_creating_customer_from_lead_with_invalid_end_date(self):
        """Negative test of creating a customer with an invalid end date."""
        response = self.client.post(
            reverse(
                "clients:customers_from_lead",
                kwargs={"lead_pk": self.lead.pk},
            ),
            {
                "first_name": self.lead.first_name,
                "last_name": self.lead.last_name,
                "phone": self.lead.phone,
                "email": self.lead.email,
                "ads": self.lead.ads.pk,
                "name": self.contract_data.name,
                "product": self.product.pk,
                "doc": self.contract_data.doc,
                "end_date": (date.today() - timedelta(days=1)).strftime("%Y-%m-%d"),
                "cost": self.contract_data.cost,
            },
        )
        self.assertContains(
            response,
            f"The end date must not be less than the start date"
            f" ({date.today().strftime("%Y-%m-%d")}).",
        )

        not_existing_contract = self.contract_qs.first()
        self.assertIsNone(not_existing_contract)
        not_existing_customer = self.customer_qs.first()
        self.assertIsNone(not_existing_customer)

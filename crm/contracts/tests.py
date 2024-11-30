from typing import Optional

from advertising.factories import ServiceFactory
from django.test import TestCase
from django.urls import reverse

from .factories import ContractFactory
from .models import Contract


class ContractsListViewTest(TestCase):
    """Test case class for testing ContractListView."""

    fixtures = [
        "services-fixtures.json",
        "contracts-fixtures.json",
    ]

    def test_get_list_contracts(self):
        """Test getting list of contracts"""
        response = self.client.get(reverse("contracts:contracts_list"))

        self.assertQuerySetEqual(
            qs=Contract.objects.order_by("pk").all(),
            values=sorted((s.pk for s in response.context["contracts"])),
            transform=lambda p: p.pk,
        )


class ContractDetailViewTest(TestCase):
    """Test case class for testing ContractDetailView."""

    def setUp(self):
        self.contract = ContractFactory.create()

    def tearDown(self):
        self.contract.delete()

    def test_get_details_about_contract(self):
        """Test getting details about the contract."""
        response = self.client.get(
            reverse("contracts:contract_detail", kwargs={"pk": self.contract.pk})
        )

        self.assertEqual(response.status_code, 200)


class ContractCreateViewTest(TestCase):
    """Test case class for testing ContractCreateView."""

    def setUp(self):
        self.contract_data = ContractFactory.build()
        self.product = ServiceFactory.create()
        self.qs = Contract.objects.filter(
            name=self.contract_data.name,
        )

        # Check that the object is being created in the test
        self.qs.delete()

        self.contract: Optional[Contract] = None

    def tearDown(self):
        self.product.delete()  # The contract will be deleted in a cascade

    def test_create_contract(self):
        """Test creating a new contract."""
        response = self.client.post(
            reverse("contracts:contract_create"),
            {
                "name": self.contract_data.name,
                "product": self.product.pk,
                "doc": self.contract_data.doc,
                "end_date": self.contract_data.end_date,
                "cost": self.contract_data.cost,
            },
        )

        self.assertRedirects(response, reverse("contracts:contracts_list"))
        self.assertTrue(self.qs.exists())

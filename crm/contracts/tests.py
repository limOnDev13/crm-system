from typing import Optional
from datetime import date, timedelta
import os

from advertising.factories import ServiceFactory
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ValidationError

from .factories import ContractFactory
from .models import Contract


def _clear_test_files():
    """Clear generated files"""
    path = settings.BASE_DIR / "upload" / "contracts"
    files = os.listdir(path)
    for filename in files:
        file_path = path / filename
        os.remove(file_path)


class ContractTestCase(TestCase):
    """Test case class for testing model Contract."""
    def setUp(self):
        self.contract_data = ContractFactory.build()
        self.product = ServiceFactory.create()

    def tearDown(self):
        self.product.delete()  # The contract will be deleted in a cascade

        _clear_test_files()

    def test_create_expired_contract(self):
        """Negative test - create an expired contract."""
        with self.assertRaises(ValidationError):
            expired_contract: Contract = Contract(
                name=self.contract_data.name,
                product=self.product,
                doc=self.contract_data.doc,
                end_date=date.today() - timedelta(days=1),
                cost=self.contract_data.cost,
            )
            expired_contract.full_clean()


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

        _clear_test_files()

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

        _clear_test_files()

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


class ContractUpdateViewTest(TestCase):
    """Test case class for testing ContractUpdateView."""

    def setUp(self):
        self.contract = ContractFactory.create()

    def tearDown(self):
        self.contract.delete()

        _clear_test_files()

    def test_update_contract(self):
        """Test updating the contract."""
        updated_contract = ContractFactory.build()
        updated_product = ServiceFactory.create()

        response = self.client.post(
            reverse(
                "contracts:contract_edit",
                kwargs={"pk": self.contract.pk},
            ),
            {
                "name": updated_contract.name,
                "product": updated_product.pk,
                "doc": updated_contract.doc,
                "end_date": updated_contract.end_date,
                "cost": updated_contract.cost,
            },
        )

        # Check redirect
        self.assertRedirects(
            response,
            reverse(
                "contracts:contract_detail",
                kwargs={"pk": self.contract.pk},
            ),
        )
        # Check that the old primary key contains updated data
        contract_: Contract = Contract.objects.filter(pk=self.contract.pk).first()
        self.assertEqual(contract_.name, updated_contract.name)
        self.assertEqual(contract_.product.pk, updated_product.pk)
        self.assertEqual(contract_.end_date, updated_contract.end_date)
        self.assertEqual(float(contract_.cost), updated_contract.cost)


class ContractDeleteViewTest(TestCase):
    """Test case class for testing ContractDeleteView."""

    def setUp(self):
        self.contract = ContractFactory.create()

    def tearDown(self):
        _clear_test_files()

    def test_delete_contract(self):
        """Test deleting the contract."""
        response = self.client.post(
            reverse(
                "contracts:contract_delete",
                kwargs={"pk": self.contract.pk},
            )
        )

        # Check redirect
        self.assertRedirects(response, reverse("contracts:contracts_list"))
        # Check that there is no data for the old primary key
        not_existing_ads = Contract.objects.filter(pk=self.contract.pk).first()
        self.assertIsNone(not_existing_ads)

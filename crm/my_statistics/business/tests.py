import random
from typing import Dict, List

from advertising.factories import AdvertisingFactory
from advertising.models import Advertising
from clients.factories import LeadFactory
from clients.models import Customer, Lead
from contracts.factories import ContractFactory
from contracts.models import Contract
from django.db import IntegrityError
from django.test import TestCase

from .statistics_logic import count_ads_customers, count_ads_lead, count_ads_profit


def _create_ads() -> List[Advertising]:
    """Create random ads."""
    return [AdvertisingFactory.create() for _ in range(10, 20)]


def _create_leads(ads: List[Advertising]) -> List[Lead]:
    """Create random leads."""
    leads: List[Lead] = list()
    for ad in ads:
        for _ in range(random.randint(0, 5)):
            lead = LeadFactory.build()
            lead.ads = ad
            lead.save()
            leads.append(lead)
    return leads


class CountAdsLeadsTest(TestCase):
    """Test case for count_ads_lead"""

    def setUp(self):
        self.ads_list = _create_ads()

    def tearDown(self):
        for ads in self.ads_list:
            ads.product.delete()

    def test_count_ads_lead(self):
        """Test counting the leads with ads"""
        ads_with_num_leads: Dict[Advertising, int] = dict()
        leads: List[Lead] = list()

        for ads in self.ads_list:
            num_leads: int = random.randint(0, 10)
            ads_with_num_leads[ads] = num_leads

            for _ in range(num_leads):
                lead = LeadFactory.build()
                lead.ads = ads
                lead.save()
                leads.append(lead)

        for ads, num_leads in ads_with_num_leads.items():
            self.assertEqual(count_ads_lead(ads), num_leads)

        for lead in leads:
            lead.delete()

    def test_count_lead_without_leads(self):
        """Test calculating the number of leads
        for an ad when there is not a single lead."""
        for ads in self.ads_list:
            self.assertEqual(count_ads_lead(ads), 0)


class CountAdsCustomersTest(TestCase):
    """Test case for count_ads_customers."""

    def setUp(self):
        self.ads_list = _create_ads()
        self.leads = _create_leads(self.ads_list)

    def tearDown(self):
        for ads in self.ads_list:
            ads.product.delete()
        for lead in self.leads:
            lead.delete()

    def test_count_ads_customers(self):
        ads_num_customers: Dict[Advertising, int] = dict()
        contracts: List[Contract] = list()

        for lead in self.leads:
            is_customer: bool = random.choice((True, False))

            if is_customer:
                while True:
                    try:
                        contract = ContractFactory.build()
                        contract.product = lead.ads.product
                        contract.save()
                        Customer.objects.create(lead=lead, contract=contract)
                    except IntegrityError:
                        pass
                    else:
                        contracts.append(contract)
                        break
                if lead.ads not in ads_num_customers:
                    ads_num_customers[lead.ads] = 1
                else:
                    ads_num_customers[lead.ads] += 1

        for ads in self.ads_list:
            self.assertEqual(count_ads_customers(ads), ads_num_customers.get(ads, 0))

        for contract in contracts:
            contract.delete()


class CountAdsProfitTest(TestCase):
    """Test case for count_ads_profit."""

    def setUp(self):
        self.ads_list = _create_ads()
        self.leads = _create_leads(self.ads_list)

    def tearDown(self):
        for ads in self.ads_list:
            ads.product.delete()
        for lead in self.leads:
            lead.delete()

    def test_count_ads_profit(self):
        ads_profit: Dict[Advertising, float] = dict()

        for lead in self.leads:
            is_customer: bool = random.choice((True, False))

            if is_customer:
                contract = ContractFactory.build()
                contract.product = lead.ads.product
                contract.save()
                Customer.objects.create(lead=lead, contract=contract)
                if lead.ads not in ads_profit:
                    ads_profit[lead.ads] = contract.cost - lead.ads.budget
                else:
                    ads_profit[lead.ads] += contract.cost

        for ads in self.ads_list:
            self.assertEqual(
                round(count_ads_profit(ads), 2),
                round(ads_profit.get(ads, -ads.budget), 2),
            )

from typing import Dict, List
import random

from django.test import TestCase
from advertising.models import Advertising
from advertising.factories import AdvertisingFactory
from clients.models import Lead
from clients.factories import LeadFactory

from .statistics_logic import count_ads_lead


class CountAdsLeadsTest(TestCase):
    """Test case for count_ads_lead"""

    def setUp(self):
        self.ads_list = [
            AdvertisingFactory.create()
            for _ in range(10, 20)
        ]

    def tearDown(self):
        for ads in self.ads_list:
            ads.delete()

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
        """A test for calculating the number of leads for an ad when there is not a single lead."""
        for ads in self.ads_list:
            self.assertEqual(count_ads_lead(ads), 0)

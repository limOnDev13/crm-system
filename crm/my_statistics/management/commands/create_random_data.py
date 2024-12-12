import random
from typing import List

from advertising.factories import AdvertisingFactory
from advertising.models import Advertising
from clients.factories import LeadFactory
from clients.models import Customer, Lead
from contracts.factories import ContractFactory
from django.core.management import BaseCommand
from django.db import IntegrityError
from services.factories import ServiceFactory
from services.models import Service


class Command(BaseCommand):
    help = "Create random data (products, ads, leads, customers, contracts)."

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating random data")

        products_count: int = random.randint(10, 50)
        self.stdout.write(f"Number products: {products_count}")
        products: List[Service] = [
            ServiceFactory.create() for _ in range(products_count)
        ]

        ads_count: int = random.randint(5, products_count)
        self.stdout.write(f"Number ads: {ads_count}")
        ads: List[Advertising] = list()
        for _ in range(ads_count):
            ad = AdvertisingFactory.build()
            ad.product = random.choice(products)
            ad.save()
            ads.append(ad)

        leads_count: int = random.randint(10, 50)
        self.stdout.write(f"Number leads: {leads_count}")
        leads: List[Lead] = list()
        for _ in range(leads_count):
            while True:
                try:
                    lead = LeadFactory.build()
                    lead.ads = random.choice(ads)
                    lead.save()
                except IntegrityError:
                    pass
                else:
                    break
            leads.append(lead)

        customers_count: int = random.randint(5, leads_count)
        self.stdout.write(f"Number customers: {customers_count}")
        for _ in range(customers_count):
            while True:
                try:
                    contract = ContractFactory.build()
                    contract.product = random.choice(products)
                    contract.save()
                except IntegrityError:
                    pass
                else:
                    break
            lead = random.choice(leads)
            leads.remove(lead)
            Customer.objects.create(lead=lead, contract=contract)

from typing import List

from advertising.models import Advertising
from clients.models import Customer, Lead
from contracts.models import Contract
from django.db.models import Subquery, Sum
from services.models import Service

from .statistics_models import AdsStatistics, TotalStatistics


def count_ads_lead(ads: Advertising) -> int:
    """Count the number of leads interested in advertising."""
    return Lead.objects.filter(ads=ads).count()


def count_ads_customers(ads: Advertising) -> int:
    """Count the number of leads who are interested
    in advertising and become active customers."""
    sub_qs = Lead.objects.filter(ads=ads).values("pk")
    return Customer.objects.filter(lead__in=Subquery(sub_qs)).count()


def count_ads_profit(ads: Advertising) -> float:
    """Calculate the profit from advertising."""
    leads_with_ads_qs = Lead.objects.filter(ads=ads).values("pk")
    customers_with_ads_qs = Customer.objects.filter(
        lead__in=Subquery(leads_with_ads_qs)
    ).values("contract")
    income = Contract.objects.filter(pk__in=Subquery(customers_with_ads_qs)).aggregate(
        Sum("cost")
    )["cost__sum"]

    income = 0 if income is None else float(income)
    expenses = float(ads.budget)

    return round(income - expenses, 2)


def ads_statistics() -> List[AdsStatistics]:
    """Get statistics on advertising."""
    ads_list: List[Advertising] = Advertising.objects.all()

    return [
        AdsStatistics(
            name=ads.name,
            leads_count=count_ads_lead(ads),
            customers_count=count_ads_customers(ads),
            profit=count_ads_profit(ads),
        )
        for ads in ads_list
    ]


def total_statistics() -> TotalStatistics:
    return TotalStatistics(
        products_count=Service.objects.count(),
        advertisements_count=Advertising.objects.count(),
        leads_count=Lead.objects.count(),
        customers_count=Customer.objects.count(),
    )

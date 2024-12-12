from typing import List

from django.db.models import Subquery

from advertising.models import Advertising
from clients.models import Lead, Customer

from .statistics_models import AdsStatistics


def count_ads_lead(ads: Advertising) -> int:
    """Count the number of leads interested in advertising."""
    return Lead.objects.filter(ads=ads).count()


def count_ads_customers(ads: Advertising) -> int:
    """Count the number of leads who are interested
     in advertising and become active customers."""
    sub_qs = Lead.objects.filter(ads=ads)
    return Customer.objects.filter(lead_in=Subquery(sub_qs)).count()


def count_ads_profit(ads: Advertising) -> float:
    """Calculate the profit from advertising."""
    leads_with_ads_qs = Lead.objects.filter(ads=ads)
    income = Customer.objects.filter(
        lead_in=Subquery(leads_with_ads_qs)
    ).values("contract").values("cost").sum()
    expenses = ads.budget
    return income - expenses


def get_ads_statistics() -> List[AdsStatistics]:
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

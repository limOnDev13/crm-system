from typing import List, Dict

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .business.statistics_logic import ads_statistics
from .business.statistics_models import AdsStatistics


def get_ads_statistics(request: HttpRequest) -> HttpResponse:
    """View function for getting statistics on ads."""
    statistics: List[AdsStatistics] = ads_statistics()
    context: Dict[str, List[AdsStatistics]] = {"ads": statistics}
    return render(request, "my_statistics/ads-statistic.html", context=context)

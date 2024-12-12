from typing import Dict, List

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .business.statistics_logic import ads_statistics, total_statistics
from .business.statistics_models import AdsStatistics, TotalStatistics


def get_ads_statistics(request: HttpRequest) -> HttpResponse:
    """View function for getting statistics on ads."""
    statistics: List[AdsStatistics] = ads_statistics()
    context: Dict[str, List[AdsStatistics]] = {"ads": statistics}
    return render(request, "my_statistics/ads-statistic.html", context=context)


def get_total_statistics(request: HttpRequest) -> HttpResponse:
    """View function for getting total statistics."""
    statistics: TotalStatistics = total_statistics()
    context: Dict[str, int] = statistics.to_dict()
    return render(request, "my_statistics/index.html", context=context)

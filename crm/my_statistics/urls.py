from django.urls import path

from .views import get_ads_statistics

app_name = "my_statistics"

urlpatterns = [
    path("ads/statistic/", get_ads_statistics, name="ads_statistics"),
]

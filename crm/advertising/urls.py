from django.urls import path

from .views import AdvertisingListView

app_name = "advertising"

urlpatterns = [
    path("ads/", AdvertisingListView.as_view(), name="ads_list"),
]

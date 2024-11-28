from django.urls import path

from .views import (
    AdvertisingListView,
    AdvertisingDetailView,
)

app_name = "advertising"

urlpatterns = [
    path("ads/", AdvertisingListView.as_view(), name="ads_list"),
    path("ads/<int:pk>/", AdvertisingDetailView.as_view(), name="ads_detail"),
]

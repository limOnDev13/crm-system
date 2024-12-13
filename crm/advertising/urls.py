from django.urls import path

from .views import (
    AdvertisingCreateView,
    AdvertisingDeleteView,
    AdvertisingDetailView,
    AdvertisingListView,
    AdvertisingUpdateView,
)

app_name = "advertising"

urlpatterns = [
    path("ads/", AdvertisingListView.as_view(), name="ads_list"),
    path("ads/new/", AdvertisingCreateView.as_view(), name="ads_create"),
    path("ads/<int:pk>/", AdvertisingDetailView.as_view(), name="ads_detail"),
    path("ads/<int:pk>/edit/", AdvertisingUpdateView.as_view(), name="ads_update"),
    path("ads/<int:pk>/delete/", AdvertisingDeleteView.as_view(), name="ads_delete"),
]

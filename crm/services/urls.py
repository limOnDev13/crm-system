from django.urls import path

from .views import (
    ServicesListView,
    ServiceDetailView,
    ServiceUpdateView,
    ServiceDeleteView,
    ServiceCreateView,
)

app_name = "services"

urlpatterns = [
    path("products/", ServicesListView.as_view(), name="services_list"),
    path("products/new/", ServiceCreateView.as_view(), name="service_create"),
    path("products/<int:pk>/", ServiceDetailView.as_view(), name="service_detail"),
    path("products/<int:pk>/edit/", ServiceUpdateView.as_view(), name="service_edit"),
    path("products/<int:pk>/delete/", ServiceDeleteView.as_view(), name="service_delete"),
]

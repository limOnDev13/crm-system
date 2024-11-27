from django.urls import path

from .views import ServicesListView, ServiceDetailView, ServiceUpdateView

app_name = "services"

urlpatterns = [
    path("products/", ServicesListView.as_view(), name="services_list"),
    path("products/<int:pk>/", ServiceDetailView.as_view(), name="service_detail"),
    path("products/<int:pk>/edit/", ServiceUpdateView.as_view(), name="service_edit"),
]

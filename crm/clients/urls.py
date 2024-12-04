from django.urls import path

from .views import (
    CustomerCreateView,
    CustomerDeleteView,
    CustomerDetailView,
    CustomersListView,
    LeadCreateView,
    LeadDeleteView,
    LeadDetailView,
    LeadsListView,
    LeadUpdateView,
    update_customer,
)

app_name = "clients"

urlpatterns = [
    path("leads/", LeadsListView.as_view(), name="leads_list"),
    path("leads/new/", LeadCreateView.as_view(), name="leads_create"),
    path("leads/<int:pk>/", LeadDetailView.as_view(), name="leads_detail"),
    path("leads/<int:pk>/edit/", LeadUpdateView.as_view(), name="leads_edit"),
    path("leads/<int:pk>/delete/", LeadDeleteView.as_view(), name="leads_delete"),
    path("customers/", CustomersListView.as_view(), name="customers_list"),
    path("customers/<int:pk>/", CustomerDetailView.as_view(), name="customers_detail"),
    path("customers/<int:pk>/edit/", update_customer, name="customers_edit"),
    path(
        "customers/<int:pk>/delete/",
        CustomerDeleteView.as_view(),
        name="customers_delete",
    ),
    path("customers/new/", CustomerCreateView.as_view(), name="customers_new"),
]

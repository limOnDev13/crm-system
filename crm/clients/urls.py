from django.urls import path

from .views import (
    LeadCreateView,
    LeadDeleteView,
    LeadDetailView,
    LeadsListView,
    LeadUpdateView,
    CustomersListView,
)

app_name = "clients"

urlpatterns = [
    path("leads/", LeadsListView.as_view(), name="leads_list"),
    path("leads/new/", LeadCreateView.as_view(), name="leads_create"),
    path("leads/<int:pk>/", LeadDetailView.as_view(), name="leads_detail"),
    path("leads/<int:pk>/edit/", LeadUpdateView.as_view(), name="leads_edit"),
    path("leads/<int:pk>/delete/", LeadDeleteView.as_view(), name="leads_delete"),
    path("customers/", CustomersListView.as_view(), name="customers_list"),
]

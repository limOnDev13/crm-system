from django.urls import path

from .views import LeadDeleteView, LeadDetailView, LeadsListView, LeadUpdateView

app_name = "clients"

urlpatterns = [
    path("leads/", LeadsListView.as_view(), name="leads_list"),
    path("leads/<int:pk>/", LeadDetailView.as_view(), name="leads_detail"),
    path("leads/<int:pk>/edit/", LeadUpdateView.as_view(), name="leads_edit"),
    path("leads/<int:pk>/delete/", LeadDeleteView.as_view(), name="leads_delete"),
]

from django.urls import path

from .views import LeadDetailView, LeadsListView

app_name = "clients"

urlpatterns = [
    path("leads/", LeadsListView.as_view(), name="leads_list"),
    path("leads/<int:pk>/", LeadDetailView.as_view(), name="leads_detail"),
]

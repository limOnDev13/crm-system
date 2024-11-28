from django.urls import path

from .views import LeadsListView

app_name = "clients"

urlpatterns = [path("leads/", LeadsListView.as_view(), name="leads_list")]

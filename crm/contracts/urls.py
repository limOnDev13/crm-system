from django.urls import path

from .views import ContractListView

app_name = "contracts"

urlpatterns = [
    path("contracts/", ContractListView.as_view(), name="contracts_list"),
]

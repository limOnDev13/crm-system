from django.urls import path

from .views import (
    ContractCreateView,
    ContractDeleteView,
    ContractDetailView,
    ContractListView,
    ContractUpdateView,
)

app_name = "contracts"

urlpatterns = [
    path("contracts/", ContractListView.as_view(), name="contracts_list"),
    path("contracts/new/", ContractCreateView.as_view(), name="contract_create"),
    path("contracts/<int:pk>/", ContractDetailView.as_view(), name="contract_detail"),
    path(
        "contracts/<int:pk>/edit/", ContractUpdateView.as_view(), name="contract_edit"
    ),
    path(
        "contracts/<int:pk>/delete/",
        ContractDeleteView.as_view(),
        name="contract_delete",
    ),
]

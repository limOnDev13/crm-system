from django.urls import path

from .views import ContractListView, ContractDetailView, ContractUpdateView

app_name = "contracts"

urlpatterns = [
    path("contracts/", ContractListView.as_view(), name="contracts_list"),
    path("contracts/<int:pk>/", ContractDetailView.as_view(), name="contract_detail"),
    path("contracts/<int:pk>/edit/", ContractUpdateView.as_view(), name="contract_edit"),
]

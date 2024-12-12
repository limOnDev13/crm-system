from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Contract


class ContractListView(PermissionRequiredMixin, ListView):
    """ListView class for getting list of contracts."""

    template_name = "contracts/contracts-list.html"
    queryset = Contract.objects.select_related("product")
    context_object_name = "contracts"
    permission_required = ("contracts.view_contract",)


class ContractDetailView(PermissionRequiredMixin, DetailView):
    """DetailView class for getting details about the contract."""

    template_name = "contracts/contracts-detail.html"
    queryset = Contract.objects.select_related("product")
    permission_required = ("contracts.view_contract",)


class ContractUpdateView(PermissionRequiredMixin, UpdateView):
    """UpdateView class for updating the contract."""

    template_name = "contracts/contracts-edit.html"
    model = Contract
    fields = "name", "product", "doc", "end_date", "cost"
    permission_required = ("contracts.change_contract",)

    def get_success_url(self):
        return reverse("contracts:contract_detail", kwargs={"pk": self.object.pk})


class ContractDeleteView(PermissionRequiredMixin, DeleteView):
    """DeleteView class for deleting the contract."""

    template_name = "contracts/contracts-delete.html"
    model = Contract
    success_url = reverse_lazy("contracts:contracts_list")
    permission_required = ("contracts.delete_contract",)


class ContractCreateView(PermissionRequiredMixin, CreateView):
    """CreateView class for creating a new contract."""

    template_name = "contracts/contracts-create.html"
    model = Contract
    fields = "name", "product", "doc", "end_date", "cost"
    success_url = reverse_lazy("contracts:contracts_list")
    permission_required = ("contracts.add_contract",)

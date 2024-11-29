from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Contract


class ContractListView(ListView):
    """ListView class for getting list of contracts."""

    template_name = "contracts/contracts-list.html"
    queryset = Contract.objects.select_related("product")
    context_object_name = "contracts"


class ContractDetailView(DetailView):
    """DetailView class for getting details about the contract."""

    template_name = "contracts/contracts-detail.html"
    queryset = Contract.objects.select_related("product")


class ContractUpdateView(UpdateView):
    """UpdateView class for updating the contract."""

    template_name = "contracts/contracts-edit.html"
    model = Contract
    fields = "name", "product", "doc", "end_date", "cost"

    def get_success_url(self):
        return reverse("contracts:contract_detail", kwargs={"pk": self.object.pk})


class ContractDeleteView(DeleteView):
    """DeleteView class for deleting the contract."""

    template_name = "contracts/contracts-delete.html"
    model = Contract
    success_url = reverse_lazy("contracts:contracts_list")

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

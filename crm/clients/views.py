from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Lead


class LeadsListView(ListView):
    """ListView class for getting list of leads."""

    template_name = "clients/leads-list.html"
    queryset = Lead.objects.select_related("ads")
    context_object_name = "leads"

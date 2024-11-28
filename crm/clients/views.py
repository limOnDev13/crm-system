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


class LeadDetailView(DetailView):
    """DetailView class for getting details about the lead."""

    template_name = "clients/leads-detail.html"
    queryset = Lead.objects.select_related("ads")


class LeadUpdateView(UpdateView):
    """UpdateView class for updating the lead."""

    template_name = "clients/leads-edit.html"
    model = Lead
    fields = "first_name", "second_name", "phone", "email", "ads"

    def get_success_url(self):
        return reverse("clients:leads_detail", kwargs={"pk": self.object.pk})


class LeadDeleteView(DeleteView):
    """DeleteView class for deleting the lead."""

    template_name = "clients/leads-delete.html"
    model = Lead
    success_url = reverse_lazy("clients:leads_list")

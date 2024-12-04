from logging import getLogger

from contracts.models import Contract
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from .forms import CustomerForm
from .models import Customer, Lead

logger = getLogger()


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


class LeadCreateView(CreateView):
    """CreateView class for creating a new lead."""

    template_name = "clients/leads-create.html"
    model = Lead
    fields = "first_name", "second_name", "phone", "email", "ads"
    success_url = reverse_lazy("clients:leads_list")


class CustomersListView(ListView):
    """ListView class for getting a list of customers."""

    template_name = "clients/customers-list.html"
    queryset = Customer.objects.select_related("lead").select_related("contract")
    context_object_name = "customers"


class CustomerDetailView(DetailView):
    """DetailView class for getting details about the customer."""

    template_name = "clients/customers-detail.html"
    queryset = Customer.objects.select_related("lead").select_related("contract")


class CustomerCreateView(FormView):
    """CreateView class for creating a new customer."""

    template_name = "clients/customers-create.html"
    success_url = reverse_lazy("clients:customers_list")
    form_class = CustomerForm

    def form_valid(self, form: CustomerForm):
        resp = super().form_valid(form)
        lead_data, contract_data = form.get_data_from_customer_form()

        lead = Lead.objects.create(**lead_data)
        contract = Contract.objects.create(**contract_data)
        Customer.objects.create(lead=lead, contract=contract)

        return resp


class CustomerDeleteView(DeleteView):
    """DeleteView for deleting the customer."""

    template_name = "clients/customers-delete.html"
    queryset = Customer.objects.select_related("lead").select_related("contract")
    success_url = reverse_lazy("clients:customers_list")


def update_customer(request: HttpRequest, pk: int) -> HttpResponse:
    """View func for updating the customer."""
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            lead_data, contract_data = form.get_data_from_customer_form()
            customer = Customer.objects.get(pk=pk)
            lead = customer.lead
            contract = customer.contract

            for key, value in lead_data.items():
                setattr(lead, key, value)
            for key, value in contract_data.items():
                setattr(contract, key, value)

            customer.lead.save()
            customer.contract.save()

            url = reverse("clients:customers_detail", kwargs={"pk": pk})
            return redirect(url)

        return redirect(request.path)

    customer = (
        Customer.objects.select_related("lead").select_related("contract").get(pk=pk)
    )
    form = CustomerForm(
        initial={
            "first_name": customer.lead.first_name,
            "last_name": customer.lead.last_name,
            "phone": customer.lead.phone,
            "email": customer.lead.email,
            "ads": customer.lead.ads,
            "name": customer.contract.name,
            "product": customer.contract.product,
            "doc": customer.contract.doc,
            "end_date": customer.contract.end_date,
            "cost": customer.contract.cost,
        }
    )
    context = {"form": form, "object": customer}
    return render(request, "clients/customers-edit.html", context=context)

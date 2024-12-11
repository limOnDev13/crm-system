from logging import getLogger
from typing import Any, Dict, List

from contracts.models import Contract
from django.db import IntegrityError, transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from .forms import CustomerBaseForm, CustomerUpdateForm, NewCustomerForm
from .models import Customer, Lead
from .utils import integrity_error_parser

logger = getLogger()


class LeadsListView(ListView):
    """ListView class for getting list of leads."""

    template_name = "clients/leads-list.html"
    queryset = Lead.objects.select_related("ads")
    context_object_name = "leads"

    def get_context_data(self, *, object_list=None, **kwargs):
        context: Dict[str, Any] = super().get_context_data(
            object_list=object_list, **kwargs
        )
        leads_pk: List[int] = [
            pk[0]
            for pk in Customer.objects.select_related("lead")
            .values_list("lead__pk")
            .all()
        ]
        context["customers_pk"] = leads_pk
        return context


class LeadDetailView(DetailView):
    """DetailView class for getting details about the lead."""

    template_name = "clients/leads-detail.html"
    queryset = Lead.objects.select_related("ads")


class LeadUpdateView(UpdateView):
    """UpdateView class for updating the lead."""

    template_name = "clients/leads-edit.html"
    model = Lead
    fields = "first_name", "last_name", "phone", "email", "ads"

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
    fields = "first_name", "last_name", "phone", "email", "ads"
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
    form_class = NewCustomerForm

    def form_valid(self, form: NewCustomerForm):
        resp = super().form_valid(form)
        lead_data, contract_data = form.get_data_from_customer_form()

        lead, _ = Lead.objects.get_or_create(**lead_data)
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
    customer = (
        Customer.objects.select_related("lead").select_related("contract").get(pk=pk)
    )
    form = CustomerUpdateForm(
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

    if request.method == "POST":
        form = CustomerUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            lead_data, contract_data = form.get_data_from_customer_form()
            customer = Customer.objects.get(pk=pk)
            lead = customer.lead
            contract = customer.contract

            try:
                with transaction.atomic():
                    for key, value in lead_data.items():
                        setattr(lead, key, value)
                    for key, value in contract_data.items():
                        setattr(contract, key, value)

                    customer.lead.save()
                    customer.contract.save()
            except IntegrityError as exc:
                field_name, exc_text = integrity_error_parser(exc, form)
                form.add_error(field_name, exc_text)
                context = {"form": form, "object": customer}
                return render(request, "clients/customers-edit.html", context=context)

            url = reverse("clients:customers_detail", kwargs={"pk": pk})
            return redirect(url)

    context = {"form": form, "object": customer}
    return render(request, "clients/customers-edit.html", context=context)


def create_customer_from_lead(request: HttpRequest, lead_pk: int) -> HttpResponse:
    """View func for updating the customer."""
    lead = get_object_or_404(Lead, pk=lead_pk)

    if request.method == "POST":
        form = CustomerBaseForm(request.POST, request.FILES)
        if form.is_valid():
            lead_data, contract_data = form.get_data_from_customer_form()

            for key, value in lead_data.items():
                setattr(lead, key, value)
            lead.save()
            contract = Contract.objects.create(**contract_data)
            Customer.objects.create(lead=lead, contract=contract)

            url = reverse("clients:customers_list")
            return redirect(url)

    if lead is not None:
        form = CustomerBaseForm(
            initial={
                "first_name": lead.first_name,
                "last_name": lead.last_name,
                "phone": lead.phone,
                "email": lead.email,
                "ads": lead.ads,
            }
        )
    else:
        form = CustomerBaseForm()
    context = {"form": form, "object": lead}
    return render(request, "clients/customers-create-from-lead.html", context=context)

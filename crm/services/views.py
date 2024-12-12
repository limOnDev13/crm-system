from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Service


class ServicesListView(PermissionRequiredMixin, ListView):
    """ListView class for getting list of services."""

    template_name = "services/products-list.html"
    model = Service
    context_object_name = "products"
    permission_required = ("services.view_service",)


class ServiceDetailView(PermissionRequiredMixin, DetailView):
    """DetailView class for getting details about the service."""

    template_name = "services/products-detail.html"
    model = Service
    permission_required = ("services.view_service",)


class ServiceUpdateView(PermissionRequiredMixin, UpdateView):
    """UpdateView class for updating the service."""

    template_name = "services/products-edit.html"
    model = Service
    fields = "name", "description", "cost"
    permission_required = ("services.change_service",)

    def get_success_url(self):
        return reverse("services:service_detail", kwargs={"pk": self.object.pk})


class ServiceDeleteView(PermissionRequiredMixin, DeleteView):
    """DeleteView class for deleting the service."""

    template_name = "services/products-delete.html"
    model = Service
    success_url = reverse_lazy("services:services_list")
    permission_required = ("services.delete_service",)


class ServiceCreateView(PermissionRequiredMixin, CreateView):
    """CreateView class for creating a new service."""

    template_name = "services/products-create.html"
    model = Service
    fields = "name", "description", "cost"
    success_url = reverse_lazy("services:services_list")
    permission_required = ("services.add_service",)

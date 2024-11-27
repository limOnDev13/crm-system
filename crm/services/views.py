from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse, reverse_lazy

from .models import Service


class ServicesListView(ListView):
    template_name = "services/products-list.html"
    model = Service
    context_object_name = "products"


class ServiceDetailView(DetailView):
    template_name = "services/products-detail.html"
    model = Service


class ServiceUpdateView(UpdateView):
    template_name = "services/products-edit.html"
    model = Service
    fields = "name", "description", "cost"

    def get_success_url(self):
        return reverse(
            "services:service_detail",
            kwargs={"pk": self.object.pk}
        )


class ServiceDeleteView(DeleteView):
    template_name = "services/products-delete.html"
    model = Service
    success_url = reverse_lazy("services:services_list")

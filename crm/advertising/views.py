from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Advertising


class AdvertisingListView(PermissionRequiredMixin, ListView):
    """ListView class for getting list of advertising."""

    template_name = "advertising/ads-list.html"
    queryset = Advertising.objects.select_related("product")
    context_object_name = "ads"
    permission_required = ("advertising.view_advertising",)


class AdvertisingDetailView(PermissionRequiredMixin, DetailView):
    """DetailView class for getting details about the advertising."""

    template_name = "advertising/ads-detail.html"
    queryset = Advertising.objects.select_related("product")
    permission_required = ("advertising.view_advertising",)


class AdvertisingUpdateView(PermissionRequiredMixin, UpdateView):
    """UpdateView class for updating the ads."""

    template_name = "advertising/ads-edit.html"
    model = Advertising
    fields = "name", "channel", "budget", "product"
    permission_required = ("advertising.change_advertising",)

    def get_success_url(self):
        return reverse("advertising:ads_detail", kwargs={"pk": self.object.pk})


class AdvertisingDeleteView(PermissionRequiredMixin, DeleteView):
    """DeleteView class for deleting the advertising."""

    template_name = "advertising/ads-delete.html"
    model = Advertising
    success_url = reverse_lazy("advertising:ads_list")
    permission_required = ("advertising.delete_advertising",)


class AdvertisingCreateView(PermissionRequiredMixin, CreateView):
    """CreateView class for creating a new advertising."""

    template_name = "advertising/ads-create.html"
    model = Advertising
    fields = "name", "channel", "budget", "product"
    success_url = reverse_lazy("advertising:ads_list")
    permission_required = ("advertising.add_advertising",)

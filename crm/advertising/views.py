from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Advertising


class AdvertisingListView(ListView):
    """ListView class for getting list of advertising."""

    template_name = "advertising/ads-list.html"
    queryset = Advertising.objects.select_related("product")
    context_object_name = "ads"


class AdvertisingDetailView(DetailView):
    """DetailView class for getting details about the advertising."""

    template_name = "advertising/ads-detail.html"
    queryset = Advertising.objects.select_related("product")


class AdvertisingUpdateView(UpdateView):
    """UpdateView class for updating the ads."""

    template_name = "advertising/ads-edit.html"
    model = Advertising
    fields = "name", "channel", "budget", "product"

    def get_success_url(self):
        return reverse("advertising:ads_detail", kwargs={"pk": self.object.pk})


class AdvertisingDeleteView(DeleteView):
    """DeleteView class for deleting the advertising."""

    template_name = "advertising/ads-delete.html"
    model = Advertising
    success_url = reverse_lazy("advertising:ads_list")


class AdvertisingCreateView(CreateView):
    """CreateView class for creating a new advertising."""

    template_name = "advertising/ads-create.html"
    model = Advertising
    fields = "name", "channel", "budget", "product"
    success_url = reverse_lazy("advertising:ads_list")

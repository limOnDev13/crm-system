from django.urls import reverse
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
    """UpdateView class for updating the service."""

    template_name = "advertising/ads-edit.html"
    model = Advertising
    fields = "name", "channel", "budget", "product"

    def get_success_url(self):
        return reverse("advertising:ads_detail", kwargs={"pk": self.object.pk})

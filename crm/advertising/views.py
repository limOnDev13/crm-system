from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
)

from .models import Advertising


class AdvertisingListView(ListView):
    """ListView class for getting list of advertising."""

    template_name = "advertising/ads-list.html"
    model = Advertising
    context_object_name = "ads"


class AdvertisingDetailView(DetailView):
    """DetailView class for getting details about the advertising."""

    template_name = "advertising/ads-detail.html"
    model = Advertising

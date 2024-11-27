from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Service


class ServicesListView(ListView):
    template_name = "services/products-list.html"
    model = Service
    context_object_name = "services"

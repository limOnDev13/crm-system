from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ServiceViewSet

app_name = "services"

routers = DefaultRouter()
routers.register("services", ServiceViewSet)

urlpatterns = [
    path("api/", include(routers.urls)),
]

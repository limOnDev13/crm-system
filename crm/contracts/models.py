from datetime import timedelta

from django.db import models
from services.models import Service


class Contract(models.Model):
    """ORM view of Contract table."""

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True,
        help_text="the unique name of the contract",
    )
    product = models.ForeignKey(
        Service, on_delete=models.CASCADE, null=False, help_text="the service provided"
    )
    doc = models.FileField(
        null=False,
        upload_to="contracts",
        help_text="the file with the contract document",
    )
    date = models.DateField(
        null=False, auto_now_add=True, help_text="date of conclusion of the contract"
    )
    duration = models.DurationField(
        null=False, default=timedelta(days=1), help_text="duration of the contract"
    )
    cost = models.DecimalField(null=False, default=0, max_digits=8, decimal_places=2)

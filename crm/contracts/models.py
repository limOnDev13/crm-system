from datetime import timedelta, datetime

from django.db import models
from django.core.exceptions import ValidationError

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
    start_date = models.DateField(
        null=False, auto_now_add=True, help_text="date of conclusion of the contract",
    )
    end_date = models.DateField(
        null=False, help_text="contract completion date",
    )
    cost = models.DecimalField(null=False, default=0, max_digits=8, decimal_places=2)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError(
                "The end date must not be less than the start date.",
                params={"start date": self.start_date, "end date": self.end_date},
            )

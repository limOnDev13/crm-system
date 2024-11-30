import os
from datetime import date

from django.core.exceptions import ValidationError
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
    start_date = models.DateField(
        null=False,
        auto_now_add=True,
        help_text="date of conclusion of the contract",
    )
    end_date = models.DateField(null=False, help_text="contract completion date")
    cost = models.DecimalField(null=False, default=0, max_digits=8, decimal_places=2)

    def clean(self):

        start_date = self.start_date

        if not start_date:
            start_date = date.today()

        if self.end_date < start_date:
            raise ValidationError(
                "The end date must not be less than the start date.",
                params={"start date": start_date, "end date": self.end_date},
            )

    def delete(self, *args, **kwargs):
        path = self.doc.path
        os.remove(path)
        super().delete(*args, **kwargs)

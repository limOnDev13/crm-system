import re

from advertising.models import Advertising
from contracts.models import Contract
from django.core.exceptions import ValidationError
from django.db import models


def validate_phone_format(value: str) -> None:
    """Validate phone format (must be like +7 (999) 000 0000)."""
    # phone must have format +7 (999) 000 0000
    if not re.match(r"\+7 \(\d{3}?\) \d{3}? \d{4}?", value):
        raise ValidationError(
            "Phone must have format +7 (999) 000 0000", params={"phone": value}
        )


class Lead(models.Model):
    """ORM view of the Lead (potential clients) table."""

    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        unique=True,
        validators=[validate_phone_format],
    )
    email = models.EmailField(null=False, unique=True)
    ads = models.ForeignKey(
        Advertising,
        null=True,
        on_delete=models.SET_NULL,
        help_text="the advertising campaign from which the"
        " lead learned about the service",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}({self.pk})"


class Customer(models.Model):
    """ORM view of the customer (potential clients) table."""

    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE)

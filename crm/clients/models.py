from advertising.models import Advertising
from contracts.models import Contract
from django.db import models

from .validators import validate_phone


class Lead(models.Model):
    """ORM view of the Lead (potential clients) table."""

    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(
        max_length=20, null=False, blank=False, unique=True, validators=[validate_phone]
    )
    email = models.EmailField(null=False, unique=True)
    ads = models.ForeignKey(
        Advertising,
        null=True,
        on_delete=models.SET_NULL,
        help_text="the advertising campaign from which the"
        " lead learned about the service",
    )


class Customer(models.Model):
    """ORM view of the customer (potential clients) table."""

    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE)

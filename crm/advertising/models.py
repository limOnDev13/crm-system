from django.db import models
from services.models import Service


class Advertising(models.Model):
    """ORM view of the Advertising table"""

    name = models.CharField(
        max_length=100, help_text="the name of the advertising campaign"
    )
    channel = models.CharField(max_length=100, help_text="promotion channel")
    budget = models.DecimalField(
        null=False,
        default=0,
        max_digits=8,
        decimal_places=2,
        help_text="advertising budget",
    )
    product = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        help_text="advertised service",
    )

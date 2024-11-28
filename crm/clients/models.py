from advertising.models import Advertising
from django.db import models


class Lead(models.Model):
    """ORM view of the PotClient (potential clients) table."""

    first_name = models.CharField(max_length=100, null=False, blank=False)
    second_name = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False, unique=True)
    email = models.EmailField(null=False, unique=True)
    ads = models.ForeignKey(
        Advertising,
        null=True,
        on_delete=models.SET_NULL,
        help_text="the advertising campaign from which the"
        " lead learned about the service",
    )

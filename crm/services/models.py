from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    cost = models.DecimalField(null=False, default=0, max_digits=8, decimal_places=2)

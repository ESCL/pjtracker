from django.db import models

from ..common.db.models import OwnedEntity


class Location(OwnedEntity):
    """
    Specific geographical location, such as address or complex.
    """
    name = models.CharField(max_length=128)
    latitude = models.DecimalField(decimal_places=7, max_digits=9, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=6, max_digits=9, null=True, blank=True)

    def __str__(self):
        return self.name

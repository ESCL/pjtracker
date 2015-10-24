from django.db import models

from ..common.models import OwnedEntity


class Nation(models.Model):

    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=2
    )
    demonym = models.CharField(
        max_length=128
    )

    def __str__(self):
        return self.name


class Region(models.Model):

    name = models.CharField(
        max_length=128
    )
    nation = models.ForeignKey(
        'Nation'
    )
    code = models.CharField(
        max_length=4
    )

    def __str__(self):
        return '{}, {}'.format(self.name, self.nation.code)


class Locality(models.Model):

    class Meta:
        verbose_name_plural = 'localities'

    name = models.CharField(
        max_length=256
    )
    region = models.ForeignKey(
        'Region'
    )

    def __str__(self):
        return '{}, {}'.format(self.name, self.region.code)


class Location(OwnedEntity):

    name = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )
    address = models.CharField(
        max_length=256
    )
    locality = models.ForeignKey(
        'Locality'
    )
    latitude = models.DecimalField(
        max_digits=12,
        decimal_places=9,
    )
    longitude = models.DecimalField(
        max_digits=12,
        decimal_places=9,
    )

    def __str__(self):
        return '{}, {}'.format(self.name or self.address, self.locality)


class Space(OwnedEntity):

    location = models.ForeignKey(
        'Location'
    )
    section = models.CharField(
        max_length=24,
        null=True,
        blank=True
    )
    identifier = models.CharField(
        max_length=24
    )

    def __str__(self):
        return '{} ({})'.format(
            '-'.join(filter(lambda x: bool(x), [self.section, self.identifier])),
            self.location
        )

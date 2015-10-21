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


class Locality(models.Model):

    name = models.CharField(
        max_length=256
    )
    region = models.ForeignKey(
        'Region'
    )


class Location(models.Model):

    name = models.CharField(
        max_length=256
    )
    address = models.CharField(
        max_length=256
    )
    locality = models.ForeignKey(
        'Locality'
    )
    latitude = models.DecimalField(
        max_digits=8
    )
    longitude = models.DecimalField(
        max_digits=8
    )


class Space(OwnedEntity):

    location = models.ForeignKey(
        'Location'
    )
    section = models.CharField(
        max_length=24
    )
    identifier = models.CharField(
        max_length=24
    )


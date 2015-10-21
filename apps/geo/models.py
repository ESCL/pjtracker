from django.db import models


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


class Location(models.Model):

    name = models.CharField(
        max_length=256
    )
    region = models.ForeignKey(
        'Region'
    )
    latitude = models.DecimalField(
        max_digits=8
    )
    longitude = models.DecimalField(
        max_digits=8
    )


class Accomodation(models.Model):

    name = models.CharField(
        max_length=256
    )
    location = models.ForeignKey(
        'Location'
    )
    section = models.CharField(
        max_length=24
    )
    room = models.CharField(
        max_length=24
    )


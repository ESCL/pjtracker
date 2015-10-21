from django.db import models

from ..common.models import OwnedEntity


class Company(OwnedEntity):

    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=8
    )


class Position(OwnedEntity):

    name = models.CharField(
        max_length=128
    )


class Status(OwnedEntity):

    owner = models.ForeignKey(
        'profiles.Account'
    )
    type = models.CharField(
        max_length=128
    )
    name = models.CharField(
        max_length=32
    )
    code = models.CharField(
        max_length=8
    )


class Employee(OwnedEntity):

    identifier = models.CharField(
        max_length=16,
    )
    first_name = models.CharField(
        max_length=64
    )
    last_name = models.CharField(
        max_length=64
    )

    # Personal data
    nationality = models.ForeignKey(
        'locations.Nation'
    )
    birth_date = models.DateField(
        null=True, blank=True
    )
    photo = models.FileField(
        max_length=256, blank=True
    )
    home_address = models.CharField(
        max_length=256, null=True, blank=True
    )

    # Organizational data (required)
    company = models.ForeignKey(
        'Company'
    )
    position = models.ForeignKey(
        'Position'
    )
    location = models.ForeignKey(
        'geo.Location'
    )
    status = models.ForeignKey(
        'Status'
    )


class Team(OwnedEntity):

    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=16,
        unique=True
    )
    company = models.ForeignKey(
        'Company'
    )
    leader = models.ForeignKey(
        'Employee',
        null=True,
        blank=True,
        related_name='teams_led'
    )

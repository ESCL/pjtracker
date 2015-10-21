from django.db import models

from ..common.models import OwnedEntity


class Company(OwnedEntity):

    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=8
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
        'organizations.Company'
    )
    leader = models.ForeignKey(
        'Employee',
        null=True,
        blank=True,
        related_name='teams_led'
    )

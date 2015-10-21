from django.db import models

from ..common.models import OwnedEntity


class Project(OwnedEntity):
    """
    Main entity used to separate the work for an account.
    """
    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=126
    )


class Phase(OwnedEntity):
    """
    Main activity classification group.
    """
    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=16
    )


class Discipline(OwnedEntity):
    """
    Second activity classification group.
    """
    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=16
    )


class Activity(OwnedEntity):
    """

    """
    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=16
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        related_name='sub_activities'
    )
    project = models.ForeignKey(
        'Project'
    )
    phase = models.ForeignKey(
        'Phase',
        null=True
    )
    discipline = models.ForeignKey(
        'Discipline',
        null=True
    )

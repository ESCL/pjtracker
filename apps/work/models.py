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
        max_length=32
    )
    location = models.ForeignKey(
        'geo.Location'
    )


class ActivityGroupType(OwnedEntity):

    name = models.CharField(
        max_length=128
    )


class ActivityGroup(OwnedEntity):

    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=16
    )
    type = models.ForeignKey(
        'ActivityGroupType'
    )


class Activity(OwnedEntity):
    """

    """
    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=32
    )
    project = models.ForeignKey(
        'Project'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        related_name='sub_activities'
    )
    groups = models.ManyToManyField(
        'ActivityGroup'
    )
    location = models.ForeignKey(
        'geo.Location',
        null=True
    )

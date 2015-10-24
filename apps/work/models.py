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

    def __str__(self):
        return self.name


class ActivityGroupType(OwnedEntity):

    name = models.CharField(
        max_length=128
    )

    def __str__(self):
        return self.name


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

    def __str__(self):
        return '{} ({})'.format(self.name, self.code)


class Activity(OwnedEntity):

    class Meta:
        verbose_name_plural = 'activities'

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
        blank=True,
        related_name='sub_activities'
    )
    groups = models.ManyToManyField(
        'ActivityGroup'
    )

    @property
    def wbs_code(self):
        if not self.parent:
            return '{}.{}'.format(self.project.code, self.code)
        return '{}.{}'.format(self.parent.wbs_code, self.code)

    def __str__(self):
        return '{} {}'.format(self.wbs_code, self.name)


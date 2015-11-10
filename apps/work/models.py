
from django.db import models

from ..common.db.models import OwnedEntity, AllowedLabourMixin
from .query import ActivityQuerySet


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

    def __str__(self):
        return self.code


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
        return self.name


class Activity(OwnedEntity, AllowedLabourMixin):

    class Meta:
        verbose_name_plural = 'activities'

    objects = ActivityQuerySet.as_manager()

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
        blank=True
    )
    groups = models.ManyToManyField(
        'ActivityGroup'
    )

    @property
    def wbs_code_parent_path(self):
        return self.parent and self.parent.wbs_code_path or [self.project.code]

    @property
    def wbs_code_path(self):
        return self.wbs_code_parent_path + [self.code]

    @property
    def wbs_code(self):
        return '.'.join(self.wbs_code_path)

    def __str__(self):
        return '{}. {}'.format(self.wbs_code, self.name)

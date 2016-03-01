
from django.db import models

from ..common.db.models import OwnedEntity
from .query import ActivityQuerySet


class Project(OwnedEntity):
    """
    Main entity used to separate the work for an account.
    """
    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=8
    )

    def __str__(self):
        return '{} ({})'.format(self.code, self.name)

    def employees_count(self):
        return self.resource_set.filter(resource_type='employee').count()

    def equipment_count(self):
        return self.resource_set.filter(resource_type='equipment').count()


class Activity(OwnedEntity):

    class Meta:
        verbose_name_plural = 'activities'

    objects = ActivityQuerySet.as_manager()

    name = models.CharField(
        max_length=64
    )
    code = models.CharField(
        max_length=4
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
        'ActivityGroup',
        blank=True
    )
    labour_types = models.ManyToManyField(
        'LabourType',
        blank=True
    )

    @property
    def full_wbs_path(self):
        return [self.project.code] + self.wbs_path

    @property
    def full_wbs_code(self):
        return '.'.join(self.full_wbs_path)

    @property
    def groups_codes(self):
        return ','.join(g.code for g in self.groups.all())

    @property
    def labour_types_codes(self):
        return ','.join(lt.code for lt in self.labour_types.all())

    @property
    def level(self):
        return len(self.wbs_path)

    @property
    def parent_wbs_path(self):
        return self.parent and self.parent.wbs_path or []

    @property
    def parent_wbs_code(self):
        return '.'.join(self.parent_wbs_path)

    @property
    def wbs_path(self):
        return self.parent_wbs_path + [self.code]

    @property
    def wbs_code(self):
        return '.'.join(self.wbs_path)

    def __str__(self):
        return '{} ({})'.format(self.code, self.name)


class ActivityGroup(OwnedEntity):

    name = models.CharField(
        max_length=64
    )
    code = models.CharField(
        max_length=4
    )
    type = models.ForeignKey(
        'ActivityGroupType'
    )

    def __str__(self):
        return '{} ({})'.format(self.code, self.name)


class ActivityGroupType(OwnedEntity):

    name = models.CharField(
        max_length=128
    )

    def __str__(self):
        return self.name


class LabourType(OwnedEntity):

    name = models.CharField(
        max_length=32
    )
    code = models.CharField(
        max_length=2
    )

    def __str__(self):
        return '{} ({})'.format(self.code, self.name)

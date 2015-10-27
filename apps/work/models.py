import itertools

from django.db import models

from ..common.db.models import OwnedEntity


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
        blank=True
    )
    groups = models.ManyToManyField(
        'ActivityGroup'
    )

    @property
    def wbs_code_prefix(self):
        if not hasattr(self, '_wbs_code_prefix'):
            self._wbs_code_prefix = self.parent and self.parent.wbs_code or self.project.code
        return self._wbs_code_prefix

    @wbs_code_prefix.setter
    def wbs_code_prefix(self, value):
        self._wbs_code_prefix = value

    @property
    def wbs_code(self):
        return '{}.{}'.format(self.wbs_code_prefix, self.code)

    def __str__(self):
        return '{} {}'.format(self.wbs_code, self.name)

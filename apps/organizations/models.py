from django.conf import settings
from django.db import models

from ..common.db.models import OwnedEntity


class Company(OwnedEntity):

    class Meta:
        verbose_name_plural = 'companies'

    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=8
    )

    def __str__(self):
        return self.code


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
    timekeepers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='timekept_teams'
    )
    supervisors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='supervised_teams'
    )
    activities = models.ManyToManyField(
        'work.Activity',
        blank=True
    )

    @property
    def employees_resources(self):
        return self.resource_set.filter(resource_type='employee')

    @property
    def employees(self):
        for r in self.employees_resources:
            yield r.employee

    @property
    def equipment_resources(self):
        return self.resource_set.filter(resource_type='equipment')

    @property
    def equipment(self):
        for r in self.equipment_resources:
            yield r.equipment

    def __str__(self):
        return self.code


class Position(OwnedEntity):

    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=3,
        null=True
    )
    labour_types = models.ManyToManyField(
        'work.LabourType',
        through='PositionLabourType'
    )

    def __str__(self):
        return self.name

    def add_labour_type(self, labour_type, user=None):
        PositionLabourType.objects.create(owner=user and user.owner, position=self,
                                          labour_type=labour_type)

    def get_labour_types_for(self, user):
        through = PositionLabourType.objects.for_user(user)
        return self.labour_types.filter(positionlabourtype__in=through)


class PositionLabourType(OwnedEntity):

    position = models.ForeignKey(
        'Position',
    )
    labour_type = models.ForeignKey(
        'work.LabourType',
    )

    def __str__(self):
        return self.labour_type

from django.db import models

from ..common.db.models import OwnedEntity, AllowedLabourMixin


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
        'auth.User',
        blank=True,
        related_name='timekept_teams'
    )
    supervisors = models.ManyToManyField(
        'auth.User',
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


class Position(OwnedEntity, AllowedLabourMixin):

    name = models.CharField(
        max_length=128
    )

    def __str__(self):
        return self.name


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
    supervisor = models.ForeignKey(
        'auth.User',
        null=True
    )
    activities = models.ManyToManyField(
        'work.Activity',
        blank=True
    )

    @property
    def employees(self):
        return self.resource_set.filter(resource_type='employee')

    @property
    def equipment(self):
        return self.resource_set.filter(resource_type='equipment')

    def __str__(self):
        return self.code


class Position(OwnedEntity, AllowedLabourMixin):

    name = models.CharField(
        max_length=128
    )

    def __str__(self):
        return self.name


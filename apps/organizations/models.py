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
        return self.name


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
        'work.Activity'
    )

    @property
    def employees(self):
        return self._get_res_iter('employee')

    @property
    def equipment(self):
        return self._get_res_iter('equipment')

    def _get_res_iter(self, resource_type):
        for res in self.resource_set.filter(resource_type=resource_type):
            yield res.instance

    def __str__(self):
        return '{} ({})'.format(self.name, self.code)


class Position(OwnedEntity):

    name = models.CharField(
        max_length=128
    )
    managerial_labour = models.BooleanField(
        default=False
    )
    indirect_labour = models.BooleanField(
        default=False
    )
    direct_labour = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.name


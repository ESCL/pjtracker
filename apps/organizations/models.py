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
        return '{} ({})'.format(self.code, self.name)


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
        return '{} ({})'.format(self.code, self.name)

    def update_resources(self, resources=None, employees=None, equipment=None):
        """
        Update the related resources from querysets of resources, employees
        and or equipment.
        """
        # Build list of ids
        if resources:
            res_ids = list(resources.values_list('id', flat=True))
        else:
            res_ids = []
            if employees:
                res_ids.extend(employees.values_list('resource_ptr_id', flat=True))
            if equipment:
                res_ids.extend(equipment.values_list('resource_ptr_id', flat=True))

        # Remove unselected and add selected resources
        self.resource_set.exclude(id__in=res_ids).update(team=None)
        self.resource_set.model.objects.filter(id__in=res_ids).update(team=self)


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
        return '{} ({})'.format(self.code, self.name)

    def add_labour_type(self, labour_type, user=None):
        PositionLabourType.objects.get_or_create(owner=user and user.owner, position=self,
                                                 labour_type=labour_type)

    def get_labour_types_for(self, user):
        through = PositionLabourType.objects.for_user(user)
        return self.labour_types.filter(positionlabourtype__in=through)

    def update_labour_types(self, labour_types, user):
        PositionLabourType.objects.filter(owner=user.owner, position=self).exclude(labour_type__in=labour_types).delete()
        for lt in labour_types:
            self.add_labour_type(lt, user)


class PositionLabourType(OwnedEntity):

    position = models.ForeignKey(
        'Position',
    )
    labour_type = models.ForeignKey(
        'work.LabourType',
    )

    def __str__(self):
        return self.labour_type.name

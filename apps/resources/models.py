from django.db import models

from ..common.db.models import OwnedEntity, History, AllowedLabourMixin
from .query import EmployeeQuerySet, EquipmentQuerySet


class EquipmentType(OwnedEntity, AllowedLabourMixin):

    name = models.CharField(
        max_length=128
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        related_name='subtypes'
    )

    def __str__(self):
        return self.name


class Resource(OwnedEntity):

    identifier = models.CharField(
        max_length=16,
    )
    company = models.ForeignKey(
        'organizations.Company'
    )
    team = models.ForeignKey(
        'organizations.Team'
    )
    project = models.ForeignKey(
        'work.Project'
    )
    resource_type = models.CharField(
        max_length=32,
    )

    @property
    def allowed_labour_types(self):
        return self.instance.allowed_labour_types

    @property
    def instance(self):
        return getattr(self, self.resource_type)

    def complete_work_log(self, work_log):
        work_log.company = self.company

    def save(self, *args, **kwargs):
        self.resource_type = self.__class__._meta.model_name
        return super(Resource, self).save(*args, **kwargs)

    def __str__(self):
        return self.instance.__str__()


class Employee(Resource):

    objects = EmployeeQuerySet.as_manager()

    first_name = models.CharField(
        max_length=64
    )
    last_name = models.CharField(
        max_length=64
    )
    birth_date = models.DateField(
        null=True, blank=True
    )
    photo = models.FileField(
        max_length=256, blank=True
    )
    home_address = models.CharField(
        max_length=256, null=True, blank=True
    )

    # Organizational data (required)
    position = models.ForeignKey(
        'organizations.Position'
    )

    @property
    def allowed_labour_types(self):
        return self.position.allowed_labour_types

    @property
    def full_name(self):
        return '{}, {}'.format(self.last_name, self.first_name)

    def complete_work_log(self, work_log):
        super(Employee, self).complete_work_log(work_log)
        work_log.position = self.position

    def __str__(self):
        return '{} ({})'.format(self.full_name, self.identifier)


class Equipment(Resource):

    class Meta:
        verbose_name_plural = 'equipment'

    objects = EquipmentQuerySet.as_manager()

    type = models.ForeignKey(
        'EquipmentType'
    )

    @property
    def allowed_labour_types(self):
        return self.type.allowed_labour_types

    def complete_work_log(self, work_log):
        super(Equipment, self).complete_work_log(work_log)
        work_log.equipment_type = self.type

    def __str__(self):
        return '{} ({})'.format(self.type, self.identifier)


class ResourceHistory(History):

    class Meta:
        abstract = True


class CompanyHistory(ResourceHistory):

    team = models.ForeignKey(
        'organizations.Company'
    )


class TeamHistory(ResourceHistory):

    team = models.ForeignKey(
        'organizations.Team'
    )


class ProjectHistory(ResourceHistory):

    team = models.ForeignKey(
        'work.Project'
    )


class PositionHistory(History):

    employee = models.ForeignKey(
        'Employee'
    )
    position = models.ForeignKey(
        'organizations.Position'
    )

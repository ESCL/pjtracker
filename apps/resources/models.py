from django.db import models

from ..common.db.models import OwnedEntity, History
from .query import EmployeeQuerySet, EquipmentQuerySet


class EquipmentType(OwnedEntity):

    name = models.CharField(
        max_length=128
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        related_name='subtypes',
    )
    labour_types = models.ManyToManyField(
        'work.LabourType',
        through='EquipmentTypeLabourType'
    )

    def __str__(self):
        return self.name

    def add_labour_type(self, labour_type, user=None):
        EquipmentTypeLabourType.objects.get_or_create(
            owner=user and user.owner, equipment_type=self,
            labour_type=labour_type
        )

    def get_labour_types_for(self, user):
        through = EquipmentTypeLabourType.objects.for_user(user)
        return self.labour_types.filter(equipmenttypelabourtype__in=through)

    def update_labour_types(self, labour_types, user):
        EquipmentTypeLabourType.objects.filter(owner=user.owner, equipment_type=self).exclude(labour_type__in=labour_types).delete()
        for lt in labour_types:
            self.add_labour_type(lt, user)


class EquipmentTypeLabourType(OwnedEntity):

    equipment_type = models.ForeignKey(
        'EquipmentType',
    )
    labour_type = models.ForeignKey(
        'work.LabourType',
    )

    def __str__(self):
        return self.labour_type


class Resource(OwnedEntity):

    identifier = models.CharField(
        max_length=16,
    )
    company = models.ForeignKey(
        'organizations.Company'
    )
    team = models.ForeignKey(
        'organizations.Team',
        null=True,
        blank=True
    )
    project = models.ForeignKey(
        'work.Project',
        null=True,
        blank=True
    )
    resource_type = models.CharField(
        max_length=32,
    )

    def get_labour_types_for(self, user):
        return self.instance.get_labour_types_for(user)

    @property
    def description(self):
        return self.instance.description

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
    gender = models.CharField(
        max_length=1,
        choices=(('F', 'Female'),
                 ('M', 'Male'))
    )
    position = models.ForeignKey(
        'organizations.Position'
    )

    @property
    def description(self):
        return self.full_name

    @property
    def full_name(self):
        return '{}, {}'.format(self.last_name, self.first_name)

    def complete_work_log(self, work_log):
        super(Employee, self).complete_work_log(work_log)
        work_log.position = self.position

    def get_labour_types_for(self, user):
        return self.position.get_labour_types_for(user)

    def __str__(self):
        return '{} ({})'.format(self.full_name, self.identifier)


class Equipment(Resource):

    class Meta:
        verbose_name_plural = 'equipment'

    objects = EquipmentQuerySet.as_manager()

    type = models.ForeignKey(
        'EquipmentType'
    )
    model = models.CharField(
        max_length=128,
        help_text="Manufacturer brand and model."
    )
    year = models.PositiveIntegerField(
        help_text="Year of manufacture."
    )

    @property
    def description(self):
        return '{} {}'.format(self.type, self.model)

    def get_labour_types_for(self, user):
        return self.type.get_labour_types_for(user)

    def complete_work_log(self, work_log):
        super(Equipment, self).complete_work_log(work_log)
        work_log.equipment_type = self.type

    def __str__(self):
        return '{} {} ({})'.format(self.model, self.type, self.identifier)


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

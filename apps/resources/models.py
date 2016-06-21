from django.db import models
from django.utils import timezone

from ..common.db.models import OwnedEntity
from .query import EmployeeQuerySet, EquipmentQuerySet


class EquipmentType(OwnedEntity):

    name = models.CharField(
        max_length=64
    )
    code = models.CharField(
        max_length=4,
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subtypes',
    )
    labour_types = models.ManyToManyField(
        'work.LabourType',
        through='EquipmentTypeLabourType'
    )

    def __str__(self):
        return '{} ({})'.format(self.name, self.code)

    def add_labour_type(self, labour_type, user=None):
        """
        Add the given labour type to this equipment type for the given user.

        :param labour_type: LabourType instance
        :param user: User instance (optional)
        :return: None
        """
        EquipmentTypeLabourType.objects.get_or_create(
            owner=user and user.owner, equipment_type=self,
            labour_type=labour_type
        )

    def get_labour_types_for(self, user):
        """
        Get queryset fo labour types for this equipment type and given user.

        :param user: User instance
        :return: LabourType queryset
        """
        through = EquipmentTypeLabourType.objects.for_user(user)
        return self.labour_types.filter(equipmenttypelabourtype__in=through)

    def update_labour_types(self, labour_types, user):
        """
        Update the labour types for this equipment type and given user.

        :param labour_types: LabourType iterable
        :param user: User instance
        :return: None
        """
        # Remove labour types that no longer match
        EquipmentTypeLabourType.objects.filter(
            owner=user.owner, equipment_type=self
        ).exclude(labour_type__in=labour_types).delete()

        # Add new ones
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


class ResourceCategory(OwnedEntity):

    class Meta:
        verbose_name_plural = 'resource categories'

    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=8
    )
    resource_type = models.CharField(
        max_length=32,
        choices=(('employee', 'Employees'),
                 ('equipment', 'Equipment'),
                 ('all', 'Both'))
    )

    def __str__(self):
        return '{} ({})'.format(self.code, self.name)


class Resource(OwnedEntity):

    identifier = models.CharField(
        max_length=16,
    )
    company = models.ForeignKey(
        'organizations.Company'
    )
    category = models.ForeignKey(
        'ResourceCategory',
        null=True,
        blank=True
    )
    team = models.ForeignKey(
        'organizations.Team',
        null=True,
        blank=True
    )
    location = models.ForeignKey(
        'geo.Location',
        null=True,
        blank=True
    )
    resource_type = models.CharField(
        max_length=32,
    )

    @property
    def project(self):
        try:
            return self.project_assignments.get(
                status=self.project_assignments.model.STATUS_APPROVED,
                start_date__lte=timezone.now().date(),
                end_date__gte=timezone.now().date(),
            )
        except self.project_assignments.model.DoesNotExist:
            return None

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
        work_log.category = self.category
        work_log.location = self.location

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
    department = models.ForeignKey(
        'organizations.Department',
        null=True,
        blank=True
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
        work_log.department = self.department
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


class ResourceProjectAssignment(OwnedEntity):
    """
    Resource assignment to a Project.
    """
    STATUS_PENDING = 'P'
    STATUS_APPROVED = 'A'
    STATUS_REJECTED = 'R'

    resource = models.ForeignKey(
        'Resource',
        related_name='project_assignments'
    )
    project = models.ForeignKey(
        'work.Project',
        related_name='resource_assignments'
    )
    start_date = models.DateField(
        db_index=True
    )
    end_date = models.DateField(
        null=True,
        db_index=True
    )
    created_by = models.ForeignKey(
        'accounts.User',
        related_name='assignments_created'
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True
    )
    reviewed_by = models.ForeignKey(
        'accounts.User',
        related_name='assignments_reviewed',
        null=True,
        blank=True
    )
    reviewed_timestamp = models.DateTimeField(
        null=True,
        blank=True
    )
    status = models.CharField(
        db_index=True,
        max_length=1,
        choices=((STATUS_PENDING, 'Pending'),
                 (STATUS_APPROVED, 'Approved'),
                 (STATUS_REJECTED, 'Rejected'))
    )

    def __str__(self):
        return '{} in {} ({}-{})'.format(self.resource, self.project,
                                         self.start_date, self.end_date)

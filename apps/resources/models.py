
from django.db import models, transaction
from django.utils import timezone

from ..common.db.models import OwnedEntity
from ..common.exceptions import NotAuthorizedError
from .query import EmployeeQuerySet, EquipmentQuerySet, ResourceProjectAssignmentQuerySet


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
            return self.projects.get(
                start_date__lte=timezone.now().date(),
                end_date__gte=timezone.now().date(),
            )
        except self.project_assignments.model.DoesNotExist:
            return None

    @property
    def assigned_projects(self):
        return self.project_assignments.filter(
            status=self.project_assignments.model.STATUS_APPROVED,
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
        return '{} {} ({})'.format(self.model, self.type.name, self.identifier)


class ResourceProjectAssignment(OwnedEntity):
    """
    Resource assignment to a Project.
    """
    STATUS_PENDING = 'P'
    STATUS_ISSUED = 'I'
    STATUS_APPROVED = 'A'
    STATUS_REJECTED = 'R'

    STATUS_ALLOWED_ACTIONS = {
        STATUS_PENDING: (('issue', 'Issue'),),
        STATUS_ISSUED: (('approve', 'Approve'),
                        ('reject', 'Reject')),
        STATUS_REJECTED: (('issue', 'Issue'),)
    }

    objects = ResourceProjectAssignmentQuerySet.as_manager()

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
        blank=True,
        null=True,
        db_index=True
    )
    timestamp = models.DateTimeField(
        default=timezone.now
    )
    status = models.CharField(
        db_index=True,
        max_length=1,
        choices=((STATUS_PENDING, 'Pending'),
                 (STATUS_ISSUED, 'Issued'),
                 (STATUS_APPROVED, 'Approved'),
                 (STATUS_REJECTED, 'Rejected')),
        default=STATUS_PENDING
    )

    @property
    def allowed_actions(self):
        return self.STATUS_ALLOWED_ACTIONS.get(self.status, [])

    @property
    def is_current(self):
        return self.start_date <= timezone.now().date() <= self.end_date

    @property
    def is_issuable(self):
        # Not sure whether this is correct, but it's very late
        return self.status != self.STATUS_APPROVED

    @property
    def is_reviewable(self):
        return self.status == self.STATUS_ISSUED

    def __str__(self):
        return '{} in {} ({}-{})'.format(self.resource, self.project,
                                         self.start_date, self.end_date)

    def approve(self, user):
        """
        Approve this assignment.

        :param user: User instance
        :return: None
        """
        # Make sure user can do this
        # Note: workaround for https://github.com/ESCL/pjtracker/issues/117
        if not user.has_perm('resources.review_resourceprojectassignment'):
            raise NotAuthorizedError('Only project managers can approve a project assignment.')

        with transaction.atomic():
            # Create related action instance
            ResourceProjectAssignmentAction.objects.create(
                assignment=self,
                actor=user,
                action=ResourceProjectAssignmentAction.APPROVED
            )

            # Set status and save
            self.status = self.STATUS_APPROVED
            self.save()

    def issue(self, user):
        """
        Issue the assignment for approval.

        :param user: User instance
        :return: None
        """
        # Make sure user can do this
        # Note: workaround for https://github.com/ESCL/pjtracker/issues/117
        if not user.has_perm('resources.issue_resourceprojectassignment'):
            raise NotAuthorizedError('Only human resource officers can issue a project assignment.')

        with transaction.atomic():
            ResourceProjectAssignmentAction.objects.create(
                assignment=self,
                actor=user,
                action=ResourceProjectAssignmentAction.ISSUED
            )
            self.status = self.STATUS_ISSUED
            self.save()

    def reject(self, user):
        """
        Reject this assignment.

        :param user: User instance
        :return: None
        """
        # Make sure user can do this
        # Note: workaround for https://github.com/ESCL/pjtracker/issues/117
        if not user.has_perm('resources.review_resourceprojectassignment'):
            raise NotAuthorizedError('Only project managers can review a project assignment.')

        with transaction.atomic():
            ResourceProjectAssignmentAction.objects.create(
                assignment=self,
                actor=user,
                action=ResourceProjectAssignmentAction.REJECTED
            )
            self.status = self.STATUS_REJECTED
            self.save()


class ResourceProjectAssignmentAction(OwnedEntity):

    ISSUED = 'I'
    REJECTED = 'R'
    APPROVED = 'A'

    assignment = models.ForeignKey(
        'ResourceProjectAssignment',
        related_name='actions'
    )
    actor = models.ForeignKey(
        'accounts.User'
    )
    action = models.CharField(
        max_length=16,
        choices=((ISSUED, 'Issued'),
                 (REJECTED, 'Rejected'),
                 (APPROVED, 'Approved'))
    )
    feedback = models.TextField(
        blank=True
    )
    timestamp = models.DateTimeField(
        default=timezone.now
    )


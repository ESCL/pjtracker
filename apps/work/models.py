
from django.db import models
from django.utils import timezone

from ..common.db.models import OwnedEntity
from .query import ActivityQuerySet


class Project(OwnedEntity):
    """
    Main entity used to separate the work for an account.
    """
    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=8
    )
    managers = models.ManyToManyField(
        'accounts.User',
        blank=True
    )

    def __str__(self):
        return '{} ({})'.format(self.code, self.name)

    @property
    def resources(self):
        return self.resource_assignments.filter(
            status=self.resource_assignments.model.STATUS_APPROVED,
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date(),
        )

    def employees_count(self):
        return self.resources.filter(
            resource__resource_type='employee',
        ).count()

    def equipment_count(self):
        return self.resources.filter(
            resource__resource_type='equipment',
        ).count()


class Activity(OwnedEntity):
    """
    Specific work entity into which hours are charged.
    """
    class Meta:
        verbose_name_plural = 'activities'

    objects = ActivityQuerySet.as_manager()

    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=6
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
        'ActivityGroup',
        blank=True
    )
    labour_types = models.ManyToManyField(
        'LabourType',
        blank=True
    )

    @property
    def full_wbs_path(self):
        return [self.project.code] + self.wbs_path

    @property
    def full_wbs_code(self):
        return '.'.join(self.full_wbs_path)

    @property
    def groups_codes(self):
        return ','.join(g.code for g in self.groups.all())

    @property
    def labour_types_codes(self):
        return ','.join(lt.code for lt in self.labour_types.all())

    @property
    def level(self):
        return len(self.wbs_path)

    @property
    def parent_wbs_path(self):
        return self.parent and self.parent.wbs_path or []

    @property
    def parent_wbs_code(self):
        return '.'.join(self.parent_wbs_path)

    @property
    def wbs_path(self):
        return self.parent_wbs_path + [self.code]

    @property
    def wbs_code(self):
        return '.'.join(self.wbs_path)

    @classmethod
    def _get_activity_and_project(cls, wbs_path):
        """
        Get the activity and project matching the given wbs path.
        If we get an activity, we use its project, otherwise we get the project.
        """
        # Get the activity using wbs_path
        activity = cls.objects.get_by_wbs_path(wbs_path)
        if activity:
            # Use activity's project
            project = activity.project

        else:
            # No activity, need to get the project
            try:
                project = Project.objects.get(code=wbs_path[0])
            except Project.DoesNotExist:
                # Ok, project's also None
                project = None

        # Return both
        return activity, project

    @staticmethod
    def _split_wbs_code(wbs_code):
        """
        Split given wbs_code in parent:child wbs paths.

        :return: tuple with wbs path for parent and code for child
        """
        # Sanity check: at least project and current wbs are required
        if '.' not in wbs_code:
            raise ValueError("WBS code format is invalid.")

        # Split in parent path (list of codes) and child code
        wbs_parts = wbs_code.split('.')
        parent = wbs_parts[:-1]
        child = wbs_parts[-1]

        # Return both
        return parent, child

    @classmethod
    def process_wbs_code_kwargs(cls, wbs_code, kwargs):
        """
        Process project, parent and code from full_wbs_code if provided.
        """
        # Get parent activity and project for the given code
        parent_path, own_code = cls._split_wbs_code(wbs_code)
        parent, project = cls._get_activity_and_project(parent_path)

        # Set code for activity
        kwargs['code'] = own_code

        # Set parent
        if not kwargs.get('parent'):
            kwargs['parent'] = parent

        # Set project (and remove creation params if existing)
        if project and not kwargs.get('project'):
            kwargs['project'] = project
            kwargs.pop('project__code', None)
            kwargs.pop('project__name', None)

    def __str__(self):
        return '{} ({})'.format(self.code, self.name)

    def __init__(self, *args, **kwargs):
        """
        Allow settings parent and project by providing a full_wbs_code.
        """
        # Pop wbs code and process kwargs if a wbs_code was passed
        wbs_code = kwargs.pop('full_wbs_code', None)
        if wbs_code:
            self.process_wbs_code_kwargs(wbs_code, kwargs)

        # Now init the other values
        super(Activity, self).__init__(*args, **kwargs)

        # Now override project and owner
        if self.parent:
            self.project = self.parent.project
            self.owner = self.project.owner


class ActivityGroup(OwnedEntity):
    """
    Entity used to group activities outside their hierarchy.
    """
    name = models.CharField(
        max_length=64
    )
    code = models.CharField(
        max_length=4
    )
    type = models.ForeignKey(
        'ActivityGroupType'
    )

    def __str__(self):
        return '{} ({})'.format(self.code, self.name)


class ActivityGroupType(OwnedEntity):
    """
    Type of activity group, to limit the groups to one of each type.
    """
    name = models.CharField(
        max_length=32
    )

    def __str__(self):
        return self.name


class LabourType(OwnedEntity):
    """
    Relation of the activity performed with direct scope progress.
    """
    name = models.CharField(
        max_length=32
    )
    code = models.CharField(
        max_length=2
    )

    def __str__(self):
        return '{} ({})'.format(self.code, self.name)

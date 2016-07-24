from datetime import datetime

from django.conf import settings
from django.db import models, transaction
from django.dispatch import Signal
from django.utils import timezone
from django.utils.functional import cached_property
from django_signals_mixin import SignalsMixin

from ..common.db.models import OwnedEntity
from ..common.exceptions import NotAuthorizedError
from .query import WorkLogQuerySet, ResourceProjectAssignmentQuerySet


class TimeSheet(SignalsMixin, OwnedEntity):
    """
    TimeSheet instance, which groups presences for a particular team and date.
    """
    CUSTOM_SIGNALS = {
        'issued': Signal(),
        'approved': Signal(),
        'rejected': Signal(),
    }

    STATUS_PREPARING = 'P'
    STATUS_ISSUED = 'I'
    STATUS_REJECTED = 'R'
    STATUS_APPROVED = 'A'

    REVIEW_POLICY_FIRST = 'F'
    REVIEW_POLICY_MAJORITY = 'M'
    REVIEW_POLICY_ALL = 'A'

    STATUS_ALLOWED_ACTIONS = {
        STATUS_PREPARING: (('issue', 'Issue'),),
        STATUS_ISSUED: (('approve', 'Approve'),
                        ('reject', 'Reject')),
        STATUS_REJECTED: (('issue', 'Issue'),)
    }

    team = models.ForeignKey(
        'organizations.Team'
    )
    date = models.DateField(
        default=datetime.today
    )
    status = models.CharField(
        max_length=1,
        choices=((STATUS_PREPARING, 'Preparing'),
                 (STATUS_ISSUED, 'Issued'),
                 (STATUS_REJECTED, 'Rejected'),
                 (STATUS_APPROVED, 'Approved')),
        default=STATUS_PREPARING
    )
    timestamp = models.DateTimeField(
        default=timezone.now
    )
    comments = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    @property
    def allowed_actions(self):
        return self.STATUS_ALLOWED_ACTIONS.get(self.status, [])

    @property
    def code(self):
        return '{}-{:%Y%m%d}'.format(self.team.code, self.date)

    @property
    def is_editable(self):
        return self.status in (self.STATUS_PREPARING, self.STATUS_REJECTED)

    @property
    def is_reviewable(self):
        return self.status in (self.STATUS_ISSUED,)

    @cached_property
    def active_reviews(self):
        """
        Return all reviews since the last issuance of the timesheet.
        """
        res = []
        for r in self.actions.order_by('-timestamp'):
            if r.action == r.ISSUED:
                break
            else:
                res.append(r)

        return list(reversed(res))

    @cached_property
    def pending_reviews(self):
        supervisors = set(self.team.supervisors.all())
        supervisors.difference_update(r.actor for r in self.active_reviews)
        return supervisors

    @cached_property
    def activities(self):
        d = {a.id: a for a in self.team.activities.all()}
        d.update({log.activity.id: log.activity
                  for log in self.work_logs.all()})
        return d

    @cached_property
    def resources(self):
        d = {r.id: r for r in self.team.resource_set.all()}
        d.update({log.resource.id: log.resource
                  for log in self.work_logs.all()})
        return d

    @cached_property
    def work_logs_data(self):
        d = {}
        for wl in self.work_logs.all():
            if wl.resource not in d:
                d[wl.resource] = {}
            d[wl.resource][wl.activity] = wl
        return d

    def __str__(self):
        return '{} - {}'.format(self.team, self.date.isoformat())

    def issue(self, user, feedback=''):
        if user not in self.team.timekeepers.all():
            raise NotAuthorizedError('Only team {} timekeepers can issue a TimeSheet.'.format(self.team))

        # Create action and update status atomically
        with transaction.atomic():
            TimeSheetAction.objects.create(
                timesheet=self,
                actor=user,
                action=TimeSheetAction.ISSUED,
                feedback=feedback
            )
            self.status = self.STATUS_ISSUED
            self.save()

        # Signal issued
        self.signal('issued')

    def reject(self, user, feedback=''):
        if user not in self.team.supervisors.all():
            raise NotAuthorizedError('Only team {} supervisor can reject a TimeSheet.'.format(self.team))

        # Create action and update status atomically
        with transaction.atomic():
            TimeSheetAction.objects.create(
                timesheet=self,
                actor=user,
                action=TimeSheetAction.REJECTED,
                feedback=feedback
            )
            updated = self.update_status('rejection', TimeSheetAction.REJECTED, self.STATUS_REJECTED)

        # Signal rejected if status was changed
        if updated:
            self.signal('rejected')

    def approve(self, user, feedback=''):
        if user not in self.team.supervisors.all():
            raise NotAuthorizedError('Only team {} supervisor can approve a TimeSheet.'.format(self.team))

        # Create action and update status atomically
        with transaction.atomic():
            TimeSheetAction.objects.create(
                timesheet=self,
                actor=user,
                action=TimeSheetAction.APPROVED,
                feedback=feedback
            )
            updated = self.update_status('approval', TimeSheetAction.APPROVED, self.STATUS_APPROVED)

        # Signal rejected if status was changed
        if updated:
            self.signal('approved')

    def update_status(self, operation, action, status):
        """
        Update the status if required and return whether it was updated or not,
        by checking that the condition to update defined by the review policy
        allows it.
        """
        # Get the total number of reviews and the ones in target status
        total_reviews = len(self.pending_reviews) + len(self.active_reviews)
        in_status = len([r for r in self.active_reviews if r.action == action])

        # Get review policy from settings
        policy = getattr(self.owner.timesheet_settings, '{}_policy'.format(operation))

        # Determine whether we can update status
        if policy == self.REVIEW_POLICY_FIRST:
            update = bool(in_status)
        elif policy == self.REVIEW_POLICY_MAJORITY:
            update = float(in_status) / total_reviews > 0.5
        else:
            update = in_status == total_reviews

        # Finally, set the status, save and return the result
        if update:
            self.status = status
            self.save()
            return True
        return False


class TimeSheetAction(SignalsMixin, OwnedEntity):

    CUSTOM_SIGNALS = {
        'executed': Signal()
    }

    ISSUED = 'I'
    REJECTED = 'R'
    APPROVED = 'A'

    timesheet = models.ForeignKey(
        'TimeSheet',
        related_name='actions'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL
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

    def save(self, *args, **kwargs):
        res = super(TimeSheetAction, self).save(*args, **kwargs)
        self.signal('executed')
        return res


class Presence(OwnedEntity):
    """
    Combination of a resource in a time sheet, used to group work logs.
    """
    class Meta:
        unique_together = ('timesheet', 'resource',)

    timesheet = models.ForeignKey(
        'TimeSheet',
    )
    resource = models.ForeignKey(
        'resources.Resource'
    )

    # De-normalization, keep attrs that can change in a resource
    company = models.ForeignKey(
        'organizations.Company'
    )
    location = models.ForeignKey(
        'geo.Location',
        null=True,
        blank=True
    )
    department = models.ForeignKey(
        'organizations.Department',
        null=True,
        blank=True
    )
    position = models.ForeignKey(
        'organizations.Position',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        'resources.ResourceCategory',
        null=True,
        blank=True
    )
    equipment_type = models.ForeignKey(
        'resources.EquipmentType',
        null=True,
        blank=True
    )


class WorkLog(OwnedEntity):
    """
    Individual charge of hours into an inactivity or activity.
    """
    objects = WorkLogQuerySet.as_manager()

    presence = models.ForeignKey(
        'Presence',
        related_name='work_logs',
        null=True
    )
    activity_base = models.ForeignKey(
        'work.ActivityBase',
        null=True
    )
    # TODO: remove after setting presence
    timesheet = models.ForeignKey(
        'TimeSheet',
        related_name='work_logs'
    )
    # TODO: remove after setting presence
    resource = models.ForeignKey(
        'resources.Resource'
    )
    # TODO: remove after setting activity_base
    activity = models.ForeignKey(
        'work.Activity',
        null=True
    )
    labour_type = models.ForeignKey(
        'work.LabourType',
    )
    hours = models.DecimalField(
        decimal_places=2,
        max_digits=4
    )

    # De-normalization, keep attrs that can change in a resource
    # TODO: remove after setting presence
    company = models.ForeignKey(
        'organizations.Company'
    )
    # TODO: remove after setting presence
    location = models.ForeignKey(
        'geo.Location',
        null=True,
        blank=True
    )
    # TODO: remove after setting presence
    department = models.ForeignKey(
        'organizations.Department',
        null=True,
        blank=True
    )
    # TODO: remove after setting presence
    position = models.ForeignKey(
        'organizations.Position',
        null=True,
        blank=True
    )
    # TODO: remove after setting presence
    category = models.ForeignKey(
        'resources.ResourceCategory',
        null=True,
        blank=True
    )
    # TODO: remove after setting presence
    equipment_type = models.ForeignKey(
        'resources.EquipmentType',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        # Update de-normalized attributes
        self.resource.instance.complete_work_log(self)
        self.owner = self.timesheet.owner

        # Save and return
        return super(WorkLog, self).save(*args, **kwargs)

    def __str__(self):
        return '{} - {}'.format(self.resource, self.activity)


class TimeSheetSettings(models.Model):
    """
    Settings for timesheets and related entities for a given account.
    """
    account = models.OneToOneField(
        'accounts.Account',
        related_name='timesheet_settings'
    )
    approval_policy = models.CharField(
        max_length=1,
        choices=((TimeSheet.REVIEW_POLICY_FIRST, 'Any'),
                 (TimeSheet.REVIEW_POLICY_MAJORITY, 'Majority'),
                 (TimeSheet.REVIEW_POLICY_ALL, 'All')),
        default=TimeSheet.REVIEW_POLICY_ALL
    )
    rejection_policy = models.CharField(
        max_length=1,
        choices=((TimeSheet.REVIEW_POLICY_FIRST, 'Any'),
                 (TimeSheet.REVIEW_POLICY_MAJORITY, 'Majority'),
                 (TimeSheet.REVIEW_POLICY_ALL, 'All')),
        default=TimeSheet.REVIEW_POLICY_FIRST
    )


class ResourceProjectAssignment(SignalsMixin, OwnedEntity):
    """
    Resource assignment to a Project.
    """
    CUSTOM_SIGNALS = {
        'issued': Signal(),
        'approved': Signal(),
        'rejected': Signal(),
    }

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
        'resources.Resource',
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
        return self.status not in (self.STATUS_APPROVED, self.STATUS_ISSUED)

    @property
    def is_rejected(self):
        return self.status == self.STATUS_REJECTED

    @cached_property
    def last_rejection(self):
        """
        Last rejection action for this assignment.
        """
        try:
            return self.actions.filter(action=ResourceProjectAssignmentAction.REJECTED).last()
        except ResourceProjectAssignmentAction.DoesNotExist:
            pass

    @property
    def is_reviewable(self):
        return self.status == self.STATUS_ISSUED

    def __str__(self):
        return '{} in {} ({}-{})'.format(self.resource, self.project,
                                         self.start_date, self.end_date)

    def approve(self, user, feedback=''):
        """
        Approve this assignment.

        :param user: User instance
        :param feedback: feedback to add to action
        :return: None
        """
        # Make sure user can do this
        # TODO: this should be in the form!
        if user not in self.project.managers.all():
            raise NotAuthorizedError('Only {} managers can approve this assignment.'.format(self.project))

        with transaction.atomic():
            # Create related action instance
            ResourceProjectAssignmentAction.objects.create(
                assignment=self,
                actor=user,
                action=ResourceProjectAssignmentAction.APPROVED,
                feedback=feedback
            )

            # Set status and save
            self.status = self.STATUS_APPROVED
            self.save()

        # Signal approval
        self.signal('approved')

    def issue(self, user, feedback=''):
        """
        Issue the assignment for approval.

        :param user: User instance
        :param feedback: feedback to add to action
        :return: None
        """
        # Make sure user can do this
        # Note: workaround for https://github.com/ESCL/pjtracker/issues/117
        # TODO: this should be in the form!
        if not user.has_perm('deployment.issue_resourceprojectassignment'):
            raise NotAuthorizedError('Only human resource officers can issue a project assignment.')

        with transaction.atomic():
            ResourceProjectAssignmentAction.objects.create(
                assignment=self,
                actor=user,
                action=ResourceProjectAssignmentAction.ISSUED,
                feedback=feedback
            )
            self.status = self.STATUS_ISSUED
            self.save()

        # Signal issued
        self.signal('issued')

    def reject(self, user, feedback=''):
        """
        Reject this assignment.

        :param user: User instance
        :param feedback: feedback to add to action
        :return: None
        """
        # Make sure user can do this
        # TODO: this should be in the form!
        if user not in self.project.managers.all():
            raise NotAuthorizedError('Only {} managers can reject this assignment.'.format(self.project))

        with transaction.atomic():
            ResourceProjectAssignmentAction.objects.create(
                assignment=self,
                actor=user,
                action=ResourceProjectAssignmentAction.REJECTED,
                feedback=feedback
            )
            self.status = self.STATUS_REJECTED
            self.save()

        # Signal rejected
        self.signal('rejected')


class ResourceProjectAssignmentAction(SignalsMixin, OwnedEntity):
    """
    Action for an assignment.
    """
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

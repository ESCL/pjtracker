from datetime import datetime

from django.conf import settings
from django.db import models
from django.dispatch import Signal
from django.utils.functional import cached_property

from ..common.db.models import OwnedEntity
from ..common.exceptions import NotAuthorizedError
from ..common.signals import SignalsMixin
from .query import WorkLogQuerySet


class TimeSheet(SignalsMixin, OwnedEntity):

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

    ALLOWED_ACTIONS = {
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
        default=datetime.utcnow
    )
    comments = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    @property
    def allowed_actions(self):
        return self.ALLOWED_ACTIONS.get(self.status, [])

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

    def issue(self, user):
        if user not in self.team.timekeepers.all():
            raise NotAuthorizedError('Only team {} timekeepers can issue a TimeSheet.'.format(self.team))

        TimeSheetAction.objects.create(
            timesheet=self,
            actor=user,
            action=TimeSheetAction.ISSUED
        )
        self.status = self.STATUS_ISSUED
        self.save()
        self.signal('issued')

    def reject(self, user):
        if user not in self.team.supervisors.all():
            raise NotAuthorizedError('Only team {} supervisor can reject a TimeSheet.'.format(self.team))

        TimeSheetAction.objects.create(
            timesheet=self,
            actor=user,
            action=TimeSheetAction.REJECTED
        )
        if self.update_status('rejection', TimeSheetAction.REJECTED, self.STATUS_REJECTED):
            self.signal('rejected')

    def approve(self, user):
        if user not in self.team.supervisors.all():
            raise NotAuthorizedError('Only team {} supervisor can approve a TimeSheet.'.format(self.team))

        TimeSheetAction.objects.create(
            timesheet=self,
            actor=user,
            action=TimeSheetAction.APPROVED
        )
        if self.update_status('approval', TimeSheetAction.APPROVED, self.STATUS_APPROVED):
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
    )
    timestamp = models.DateTimeField(
        default=datetime.utcnow
    )

    def save(self, *args, **kwargs):
        res = super(TimeSheetAction, self).save(*args, **kwargs)
        self.signal('executed')
        return res


class WorkLog(OwnedEntity):

    objects = WorkLogQuerySet.as_manager()

    timesheet = models.ForeignKey(
        'TimeSheet',
        related_name='work_logs'
    )
    resource = models.ForeignKey(
        'resources.Resource'
    )
    activity = models.ForeignKey(
        'work.Activity',
        null=True,
        blank=True
    )
    labour_type = models.ForeignKey(
        'work.LabourType',
    )
    hours = models.DecimalField(
        decimal_places=2,
        max_digits=4
    )

    # De-normalization, keep attrs that can change in an employee
    company = models.ForeignKey('organizations.Company')
    position = models.ForeignKey(
        'organizations.Position',
        null=True
    )
    equipment_type = models.ForeignKey(
        'resources.EquipmentType',
        null=True
    )

    def save(self, *args, **kwargs):
        # Update de-normalized attributes
        self.resource.instance.complete_work_log(self)

        # Save and return
        return super(WorkLog, self).save(*args, **kwargs)

    def __str__(self):
        return '{} - {}'.format(self.resource, self.activity)


class TimeSheetSettings(models.Model):
    """
    Settings for timesheets and related entities for a given account.
    """
    # TODO: Validate poilicies, they must be different to avoid status limbo!!!
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

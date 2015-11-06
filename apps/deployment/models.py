from datetime import datetime

from django.db import models
from django.dispatch import Signal
from django.utils.functional import cached_property

from ..common.db.models import OwnedEntity, LabourType
from ..common.signals import SignalsMixin


class TimeSheet(OwnedEntity, SignalsMixin):

    CUSTOM_SIGNALS = {
        'issued': Signal(),
        'approved': Signal(),
        'rejected': Signal(),
    }

    STATUS_PREPARING = 'P'
    STATUS_ISSUED = 'I'
    STATUS_REJECTED = 'R'
    STATUS_APPROVED = 'A'

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
    issuer = models.ForeignKey(
        'auth.User',
        related_name='timesheets_issued',
        null=True
    )
    reviewer = models.ForeignKey(
        'auth.User',
        related_name='timesheets_reviewed',
        null=True,
        blank=True
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
    def code(self):
        return '{}-{:%Y%m%d}'.format(self.team.code, self.date)

    @cached_property
    def resources(self):
        d = {r.id: r for r in self.team.resource_set.all()}
        d.update({log.resource.id: log.resource
                  for log in self.work_logs.all()})
        return d

    @cached_property
    def activities(self):
        d = {a.id: a for a in self.team.activities.all()}
        d.update({log.activity.id: log.activity
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
        self.status = self.STATUS_ISSUED
        self.issuer = user
        self.save()
        self.signal('issued')

    def reject(self, user):
        if user != self.team.supervisor:
            raise TypeError('Only team {} supervisor can reject a TimeSheet.'.format(self.team))

        self.status = self.STATUS_REJECTED
        self.reviewer = user
        self.save()
        self.signal('rejected')

    def approve(self, user):
        if user != self.team.supervisor:
            raise TypeError('Only team {} supervisor can approve a TimeSheet.'.format(self.team))

        self.status = self.STATUS_APPROVED
        self.reviewer = user
        self.save()
        self.signal('approved')


class WorkLog(models.Model):

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
    labour_type = models.CharField(
        max_length=1,
        choices=LabourType.CHOICES
    )
    hours = models.DecimalField(
        decimal_places=2,
        max_digits=4
    )

    # De-normalization, keep attrs that can change in an employee
    company = models.ForeignKey('organizations.Company')
    location = models.ForeignKey('geo.Location')
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

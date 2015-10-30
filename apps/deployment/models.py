from datetime import datetime

from django.db import models
from django.dispatch import Signal

from ..common.db.models import OwnedEntity
from ..common.signals import SignalsMixin


class TimeSheet(OwnedEntity, SignalsMixin):

    SIGNALS = {
        'issued': Signal(providing_args=['target']),
        'approved': Signal(providing_args=['target']),
        'rejected': Signal(providing_args=['target']),
        'read': Signal(providing_args=['target'])
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
        null=True
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

    LABOUR_INDIRECT = 'I'
    LABOUR_DIRECT = 'D'
    LABOUR_MANAGERIAL = 'M'

    timesheet = models.ForeignKey(
        'TimeSheet',
        related_name='work_logs'
    )
    employee = models.ForeignKey(
        'resources.Employee'
    )
    activity = models.ForeignKey(
        'work.Activity',
        null=True,
        blank=True
    )
    labour_type = models.CharField(
        max_length=1,
        choices=((LABOUR_INDIRECT, 'Indirect'),
                 (LABOUR_DIRECT, 'Direct'),
                 (LABOUR_MANAGERIAL, 'Managerial'))
    )
    hours = models.DecimalField(
        decimal_places=2,
        max_digits=4
    )

    # De-normalization, keep attrs that can change in an employee
    company = models.ForeignKey('organizations.Company')
    position = models.ForeignKey('organizations.Position')
    location = models.ForeignKey('geo.Location')

    def save(self, *args, **kwargs):
        # Update de-normalized attributes
        self.company = self.employee.company
        self.position = self.employee.position
        self.location = self.employee.location

        # Save and return
        return super(WorkLog, self).save(*args, **kwargs)

    def __str__(self):
        return '{} - {}'.format(self.employee, self.activity)
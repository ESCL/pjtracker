from datetime import datetime

from django.db import models

from ..common.models import OwnedEntity


class TimeSheet(OwnedEntity):

    STATUS_PREPARING = 'P'
    STATUS_ISSUED = 'I'
    STATUS_REJECTED = 'R'
    STATUS_APPROVED = 'A'

    team = models.ForeignKey(
        'organizations.Team'
    )
    date = models.DateField(
    )
    status = models.CharField(
        max_length=1,
        choices=((STATUS_PREPARING, 'Preparing'),
                 (STATUS_ISSUED, 'Issued'),
                 (STATUS_REJECTED, 'Rejected'),
                 (STATUS_APPROVED, 'Approved'))
    )
    issuer = models.ForeignKey(
        'auth.User'
    )
    timestamp = models.DateTimeField(
        default=datetime.utcnow
    )
    comments = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    def __str__(self):
        return '{} - {}'.format(self.team, self.date.isoformat())


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
    position = models.ForeignKey('resources.Position')
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
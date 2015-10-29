__author__ = 'kako'

from ..notifications.models import Notification
from .models import TimeSheet


def notify_timesheet_issued(sender, target, type, **kwargs):
    Notification.objects.create(
        recipient=target.team.supervisor,
        event_target=target,
        event_type=type,
        title='TimeSheet Issued'
    )


def notify_timesheet_rejected(sender, target, type, **kwargs):
    Notification.objects.create(
        recipient=target.issuer,
        event_target=target,
        event_type=type,
        title='TimeSheet Issued'
    )


def notify_timesheet_approved(sender, target, type, **kwargs):
    Notification.objects.create(
        recipient=target.issuer,
        event_target=target,
        event_type=type,
        title='TimeSheet Issued'
    )


TimeSheet.on_signal('issued', notify_timesheet_issued)
TimeSheet.on_signal('rejected', notify_timesheet_rejected)
TimeSheet.on_signal('approved', notify_timesheet_approved)


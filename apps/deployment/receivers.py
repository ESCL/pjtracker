__author__ = 'kako'

import itertools

from ..notifications.models import Notification
from .models import TimeSheet


TS_MESSAGE_TEMPLATE = "A timesheet for the team {{ target.team }} " \
                      "corresponding to the day {{ target.date }} has been " \
                      "{{ event }}."


def notify_timesheet_issued(sender, instance, name=None, **kwargs):
    for supervisor in instance.team.supervisors.all():
        Notification.objects.create(
            recipient=supervisor,
            event_target=instance,
            event_type=name,
            title='TimeSheet Issued',
            message_template=TS_MESSAGE_TEMPLATE
        )


def notify_timesheet_rejected(sender, instance, name=None, **kwargs):
    timekeepers = instance.team.timekeepers.all()
    reviewers = (r.actor for r in instance.active_reviews)
    for timekeeper in itertools.chain(timekeepers, reviewers):
        Notification.objects.create(
            recipient=timekeeper,
            event_target=instance,
            event_type=name,
            title='TimeSheet Rejected',
            message_template=TS_MESSAGE_TEMPLATE
        )


TimeSheet.on_signal('issued', notify_timesheet_issued)
TimeSheet.on_signal('rejected', notify_timesheet_rejected)
#TimeSheet.on_signal('approved', notify_timesheet_issuer)

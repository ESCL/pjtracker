__author__ = 'kako'

from ..notifications.models import Notification
from .models import TimeSheet

TS_MESSAGE_TEMPLATE = "A timesheet for the team {{ target.team }} corresponding to the day {{ target.date }} has been {{ event }}."

def notify_timesheet_supervisor(sender, target, type, **kwargs):
    title = 'TimeSheet {}'.format(type.title())
    Notification.objects.create(
        recipient=target.team.supervisor,
        event_target=target,
        event_type=type,
        title=title,
        message_template=TS_MESSAGE_TEMPLATE
    )


def notify_timesheet_issuer(sender, target, type, **kwargs):
    title = 'TimeSheet {}'.format(type.title())
    Notification.objects.create(
        recipient=target.issuer,
        event_target=target,
        event_type=type,
        title=title,
        message_template=TS_MESSAGE_TEMPLATE
    )


TimeSheet.on_signal('issued', notify_timesheet_supervisor)
TimeSheet.on_signal('rejected', notify_timesheet_issuer)
TimeSheet.on_signal('approved', notify_timesheet_issuer)


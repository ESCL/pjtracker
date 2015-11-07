__author__ = 'kako'

from ..accounts.models import Account
from ..notifications.models import Notification
from .models import TimeSheet, TimeSheetSettings


TS_MESSAGE_TEMPLATE = "A timesheet for the team {{ target.team }} " \
                      "corresponding to the day {{ target.date }} has been " \
                      "{{ event }}."


def ensure_settings(sender, instance, created, **kwargs):
    """
    Ensure the existence of timesheet settings for the given account.
    """
    # TODO: Notify users can set stuff up properly if it was created
    TimeSheetSettings.objects.get_or_create(account=instance)


def notify_timesheet_issued(sender, instance, name=None, **kwargs):
    """
    Notify team supervisors that a timesheet has been issued.
    """
    for supervisor in instance.team.supervisors.all():
        Notification.objects.create(
            recipient=supervisor,
            event_target=instance,
            event_type=name,
            title='TimeSheet Issued',
            message_template=TS_MESSAGE_TEMPLATE
        )


def notify_timesheet_rejected(sender, instance, name=None, **kwargs):
    """
    Notify team timekeepers and supervisors that have reviewed the timesheet
    that the timesheet has been rejected.
    """
    recipients = set(instance.team.timekeepers.all())
    recipients.update(r.actor for r in instance.active_reviews)
    for recipient in recipients:
        Notification.objects.create(
            recipient=recipient,
            event_target=instance,
            event_type=name,
            title='TimeSheet Rejected',
            message_template=TS_MESSAGE_TEMPLATE
        )


# Account creation listeners
Account.on_signal('saved', ensure_settings)

# Timesheet workflow listeners
TimeSheet.on_signal('issued', notify_timesheet_issued)
TimeSheet.on_signal('rejected', notify_timesheet_rejected)


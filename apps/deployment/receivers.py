__author__ = 'kako'

from django.contrib.contenttypes.models import ContentType

from ..accounts.models import Account
from ..notifications.models import Notification
from .models import TimeSheet, TimeSheetAction, TimeSheetSettings


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
            message_template="A timesheet for the team {{ target.team }} corresponding "
                             "to the day {{ target.date }} has been {{ event }}. Your "
                             "review is pending.",
            action_label='Review',
            action_url="{% url 'timesheet-action' pk=target.pk action='add' %}"
        )


def notify_timesheet_rejected(sender, instance, name=None, **kwargs):
    """
    Notify team timekeepers and supervisors that have reviewed the timesheet
    that the timesheet has been rejected.
    """
    recipients = set(instance.team.timekeepers.all())
    for recipient in recipients:
        Notification.objects.create(
            recipient=recipient,
            event_target=instance,
            event_type=name,
            title='TimeSheet Rejected',
            message_template="A timesheet for the team {{ target.team }} corresponding "
                             "to the day {{ target.date }} has been {{ event }}. Your "
                             "correction and re-issuance are required.",
            action_label='Correct',
            action_url="{% url 'timesheet' pk=target.pk action='edit' %}",
        )


def expire_issued_notifications(sender, instance, name=None, **kwargs):
    """
    Expire "issued" notifications, which depending on the action will be all
    notifications for a timesheet or just the ones for the actor.
    """
    # Start building filters, restrict to TimeSheet.issued
    ct_ts = ContentType.objects.get_for_model(TimeSheet)
    filters = {'event_target_model': ct_ts,
               'event_type': 'issued'}

    if isinstance(instance, TimeSheet):
        # Timesheet status changed: restrict to this timesheet
        filters['event_target_id'] = instance.id

    elif isinstance(instance, TimeSheetAction):
        # Supervisor reviewed: restrict the action's timesheet and this supervisor
        filters['event_target_id'] = instance.timesheet.id
        filters['recipient'] = instance.actor

    else:
        # WTF? No idea what to do
        raise TypeError('Cannot process for instance {}.'.format(instance))

    # Finally, expire them
    Notification.objects.filter(**filters).update(status=Notification.STATUS_EXPIRED)


# Account creation listeners
Account.on_signal('saved', ensure_settings)

# Timesheet workflow listeners
TimeSheetAction.on_signal('reviewed', expire_issued_notifications)
TimeSheet.on_signal('issued', notify_timesheet_issued)
TimeSheet.on_signal('rejected', notify_timesheet_rejected)
TimeSheet.on_signal('rejected', expire_issued_notifications)
TimeSheet.on_signal('approved', expire_issued_notifications)


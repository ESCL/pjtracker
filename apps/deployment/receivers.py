from django.contrib.contenttypes.models import ContentType

from ..accounts.models import Account
from ..notifications.models import Notification
from .models import (TimeSheet, TimeSheetAction, TimeSheetSettings,
                     ResourceProjectAssignment, ResourceProjectAssignmentAction)


def disable_assignment_notifications(sender, instance, name=None, **kwargs):
    """
    Expire "issued" notifications for assignments for all recipients.
    """
    # Get assignment content type
    ct_rpa = ContentType.objects.get_for_model(ResourceProjectAssignment)

    # Disable notifications for this assignment
    notifs = Notification.objects.enabled().filter(
        event_target_model=ct_rpa,
        event_target_id=instance.id
    )

    # Finally, disable them
    notifs.update(status=Notification.STATUS_DISABLED)


def disable_timesheet_notifications(sender, instance, name=None, **kwargs):
    """
    Expire notifications, which might be for all recipients or only the actor,
    depending on the action.
    """
    # Start building filters, restrict to TimeSheet model
    ct_ts = ContentType.objects.get_for_model(TimeSheet)
    filters = {'event_target_model': ct_ts}

    if isinstance(instance, TimeSheetAction):
        # User did something: clear notifs for current user and timesheet
        filters['event_target_id'] = instance.timesheet.id
        filters['recipient'] = instance.actor

    elif isinstance(instance, TimeSheet):
        # Timesheet status changed: clear all notifs for timesheet
        filters['event_target_id'] = instance.id

    else:
        # WTF? No idea what to do
        raise TypeError('Cannot process for instance {}.'.format(instance))

    # Disable all selected notifs
    Notification.objects.enabled().filter(**filters).update(status=Notification.STATUS_DISABLED)


def ensure_settings(sender, instance, created, **kwargs):
    """
    Ensure the existence of timesheet settings for the given account.
    """
    # TODO: Notify users can set stuff up properly if it was created
    TimeSheetSettings.objects.get_or_create(account=instance)


def notify_assignment_issued(sender, instance, name=None, **kwargs):
    """
    Notify project managers that HR attempted to assign a new resource
    to the projcet.
    """
    # Iterate all managers
    for manager in instance.project.managers.all():
        # Build action url for template
        action_url = "{{% url '{}-project-action' parent_pk=target.resource.instance.pk " \
                     "pk=target.pk %}}".format(instance.resource.resource_type)

        # Create notification instance
        Notification.objects.create(
            recipient=manager,
            event_target=instance,
            event_type=name,
            title='Project Assignment Issued',
            message_template="{{ target.resource }} is being assigned to {{ target.project }}."
                             "Your review is pending.",
            action_label='Review',
            action_url=action_url
        )


def notify_assignment_rejected(sender, instance, name=None, **kwargs):
    """
    Notify HR personnel that the resource assignment was rejected by a
    project manager.
    """
    # Get current issuance (last issued action)
    issuance = instance.actions.filter(action=ResourceProjectAssignmentAction.ISSUED).last()

    # Build action url for template
    action_url = "{{% url '{}-project' parent_pk=target.resource.instance.pk " \
                 "pk=target.pk action='edit' %}}".format(instance.resource.resource_type)

    # Create notification instance
    Notification.objects.create(
        recipient=issuance.actor,
        event_target=instance,
        event_type=name,
        title='Project Assignment Rejected',
        message_template="The assignment of {{ target.resource }} to project "
                         "{{ target.project }} was rejected. Your correction and "
                         "re-issuance are required.",
        action_label='Correct',
        action_url=action_url
    )


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
    for timekeeper in instance.team.timekeepers.all():
        Notification.objects.create(
            recipient=timekeeper,
            event_target=instance,
            event_type=name,
            title='TimeSheet Rejected',
            message_template="A timesheet for the team {{ target.team }} corresponding "
                             "to the day {{ target.date }} has been {{ event }}. Your "
                             "correction and re-issuance are required.",
            action_label='Correct',
            action_url="{% url 'timesheet' pk=target.pk action='edit' %}",
        )


# Account saved: ensure settings
Account.on_signal('saved', ensure_settings)

# Resource project assignment issued: clear and notify again
ResourceProjectAssignment.on_signal('issued', disable_assignment_notifications)
ResourceProjectAssignment.on_signal('issued', notify_assignment_issued)

# Resource project assignment rejected: clear and notify again
ResourceProjectAssignment.on_signal('rejected', disable_assignment_notifications)
ResourceProjectAssignment.on_signal('rejected', notify_assignment_rejected)

# Resource project assignment approved: clear only (closure is silent)
ResourceProjectAssignment.on_signal('approved', disable_assignment_notifications)

# Timesheet action (any): clear for action actor only
TimeSheetAction.on_signal('executed', disable_timesheet_notifications)

# Timesheet issued: clear and notify again
TimeSheet.on_signal('issued', disable_timesheet_notifications)
TimeSheet.on_signal('issued', notify_timesheet_issued)

# Timesheet rejected: clear and notify again
TimeSheet.on_signal('rejected', disable_timesheet_notifications)
TimeSheet.on_signal('rejected', notify_timesheet_rejected)

# Timesheet approved: clear only (closure is silent)
TimeSheet.on_signal('approved', disable_timesheet_notifications)

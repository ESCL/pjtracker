
from datetime import datetime

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.dispatch import Signal
from django.template import Template, Context

from .query import NotificationQuerySet
from ..common.signals import SignalsMixin


class Notification(models.Model, SignalsMixin):

    SIGNALS = {
        'read': Signal(providing_args=['target'])
    }

    STATUS_ENABLED = 'E'
    STATUS_DISMISSED = 'D'

    objects = NotificationQuerySet.as_manager()

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL
    )
    event_target_model = models.ForeignKey(
        ContentType
    )
    event_target_id = models.PositiveIntegerField(
    )
    event_target = GenericForeignKey(
        'event_target_model',
        'event_target_id'
    )
    event_type = models.CharField(
        max_length=16
    )
    title = models.CharField(
        max_length=128
    )
    message_template = models.TextField(
    )
    timestamp = models.DateTimeField(
        default=datetime.utcnow
    )
    status = models.CharField(
        max_length=1,
        choices=((STATUS_ENABLED, 'Active'),
                 (STATUS_DISMISSED, 'Dismissed')),
        default=STATUS_ENABLED
    )

    @property
    def is_enabled(self):
        return self.status == self.STATUS_ENABLED

    @property
    def message(self):
        return Template(self.message_template).render(Context(
            {'target': self.event_target, 'event': self.event_type}
        ))

    def dismiss(self):
        self.status = self.STATUS_DISMISSED
        self.save()
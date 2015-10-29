
from datetime import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Notification(models.Model):

    recipient = models.ForeignKey(
        'auth.User'
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
    message = models.TextField(
    )
    timestamp = models.DateTimeField(
        default=datetime.utcnow
    )

__author__ = 'kako'

from django.db import models

from .query import OwnedEntityQuerySet


class OwnedEntity(models.Model):
    """
    Base class for all entities that are "owned" by an account.

    The field "owner" is nullable because we probably want "global" objects
    even for some ownable types (ie, locations).
    """
    class Meta:
        abstract = True

    objects = OwnedEntityQuerySet.as_manager()

    owner = models.ForeignKey(
        'accounts.Account',
        null=True,
        blank=True
    )


class History(models.Model):
    """
    Base class for all entities that store transitions, optimized to fetch
    values at specific date-times.
    """
    class Meta:
        abstract = True

    start = models.DateTimeField()
    end = models.DateTimeField()

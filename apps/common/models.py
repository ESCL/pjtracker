__author__ = 'kako'

from django.db import models

from .query import OwnedEntityQuerySet


class OwnedEntityMeta(type):

    def __new__(cls, *args, **kwargs):
        mgr = kwargs.get('objects')
        if mgr and not isinstance(mgr.get_queryset(), OwnedEntityQuerySet):
            raise TypeError("OwnedEntity model managers must use an "
                            "OwnedEntityQuerySet.")
        elif not mgr:
            kwargs['objects'] = OwnedEntityQuerySet.as_manager()

        return super(OwnedEntityMeta, cls).__new__(*args, **kwargs)


class OwnedEntity(models.Model):
    """
    Base class for all entities that are "owned" by an account.

    The field "owner" is nullable because we probably want "global" objects
    even for some ownable types (ie, locations).
    """
    __metaclass__ = OwnedEntityMeta

    class Meta:
        abstract = True

    owner = models.ForeignKey(
        'accounts.Account',
        null=True
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


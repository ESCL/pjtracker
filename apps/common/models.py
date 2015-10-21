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
    """
    __metaclass__ = OwnedEntityMeta

    class Meta:
        abstract = True

    owner = models.ForeignKey(
        'profiles.Account',
        null=True
    )
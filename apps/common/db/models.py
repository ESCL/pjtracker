__author__ = 'kako'

from django.db import models

from .query import OwnedEntityQuerySet


class ValuesObject(object):
    """
    Generic object that constructs related objects like a Django model
    from queryset values() data. This is used as a workaround for Django's
    shitty behaviour of returning dicts instead of instances when using
    values() to group.

    Example usage:
        vo = ValuesObject({'id': 1, 'related__id': 1, 'related__name': 'lolwut?'},
                          related=RelatedModel)
        print(vo.related.name)
        lolwut?
    """
    def __init__(self, values, **related):
        self._values = values
        self._related = related
        self._build_data()
        self._populate_attrs()

    def _build_data(self):
        self._data = {}
        for k, v in self._values.items():
            attrs = k.split('__')
            first_attr = attrs[0]
            if len(attrs) > 1:
                if first_attr not in self._data:
                    self._data[first_attr] = {}
                for attr in attrs[1:]:
                    self._data[first_attr][attr] = v

            else:
                self._data[k] = v

    def _populate_attrs(self):
        for k, v in self._data.items():
            if k in self._related:
                v = self._related[k](**v)
            setattr(self, k, v)


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

__author__ = 'kako'

from django.db.models.query import QuerySet


class OwnedEntityQuerySet(QuerySet):

    def filter(self, *args, **kwargs):
        return super(OwnedEntityQuerySet, self).filter(*args, **kwargs)

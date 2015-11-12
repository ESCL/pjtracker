__author__ = 'kako'

from django.db.models import Count
from ..common.db.query import OwnedEntityQuerySet


class ActivityQuerySet(OwnedEntityQuerySet):

    def workable(self):
        """
        Filter the activities that can charge hours on any labour type.
        """
        return self.annotate(Count('labour_types')).filter(labour_types__count__gt=0)


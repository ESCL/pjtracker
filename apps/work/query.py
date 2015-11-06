__author__ = 'kako'

from django.db.models import Q
from ..common.db.query import OwnedEntityQuerySet


class ActivityQuerySet(OwnedEntityQuerySet):

    def workable(self):
        """
        Filter the activities that can charge hours on any labour type.
        """
        return self.filter(Q(managerial_labour=True)|
                           Q(indirect_labour=True)|
                           Q(direct_labour=True))

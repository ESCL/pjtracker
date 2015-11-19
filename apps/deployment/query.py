__author__ = 'kako'


from ..common.db.query import OwnedEntityQuerySet, ValuesGroupMixin


class WorkLogQuerySet(ValuesGroupMixin, OwnedEntityQuerySet):
    pass


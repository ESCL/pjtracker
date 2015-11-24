__author__ = 'kako'

from django.contrib.auth.models import UserManager as UserManagerBase

from ..common.db.query import OwnedEntityQuerySet


class UserManager(UserManagerBase):
    _queryset_class = OwnedEntityQuerySet

    def for_user(self, user, *args, **kwargs):
        if user.domain:
            return self.get_queryset().filter(owner=user.domain)
        return self


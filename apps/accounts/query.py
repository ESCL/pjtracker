__author__ = 'kako'

from django.contrib.auth.models import UserManager as UserManagerBase

from ..common.db.query import OwnedEntityQuerySet


class UserQuerySet(OwnedEntityQuerySet):
    include_global = False


class UserManager(UserManagerBase):
    _queryset_class = UserQuerySet

    def for_user(self, *args, **kwargs):
        return self.get_queryset().for_user(*args, **kwargs)
    
    def get_or_create(self, *args, **kwargs):
        """
        Handle username update to make sure match is correct.
        """
        if 'username' in kwargs:
            kwargs['username'] = self.model.build_username(kwargs['username'],
                                                           kwargs.get('owner'))
        return super(UserManager, self).get_or_create(*args, **kwargs)


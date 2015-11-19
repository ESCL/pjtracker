import inspect

from django.contrib.auth.models import AbstractUser
from django.db import models

from ..common.signals import SignalsMixin
from .query import UserManager


class Account(models.Model, SignalsMixin):

    TIMESHEET_REVIEW_ANY = 'any'
    TIMESHEET_REVIEW_MAJORITY = 'majority'
    TIMESHEET_REVIEW_ALL = 'all'

    name = models.CharField(
        max_length=128
    )

    def __str__(self):
        return self.name


class User(AbstractUser):

    owner = models.ForeignKey(
        'Account',
        null=True
    )

    objects = UserManager()

    @property
    def domain(self):
        if self.is_staff or self.is_superuser:
            return None
        return self.owner

    def __str__(self):
        return '{} ({})'.format(self.username, self.get_full_name())

    def _classify(self, obj):
        if not inspect.isclass(obj):
            obj = type(obj)
        return obj

    def get_allowed_actions_for(self, obj):
        """
        Return a list of actions that can be executed by the user, which
        consist of a tuple with action name, and optionally a field name.
        """
        actions = []
        obj = self._classify(obj)

        for permcode in self.get_all_permissions():
            app, perm = permcode.split('.')
            action = perm.split('_', 2)
            model_name = action.pop(1)
            if model_name == obj._meta.model_name:
                actions.append(tuple(action))

        return actions

    def get_disallowed_fields_for(self, obj):
        """
        Return a set of fields that the user cannot modify.
        """
        disallowed = set(self._classify(obj)._meta.get_all_field_names())
        for action in self.get_allowed_actions_for(obj):
            try:
                disallowed.remove(action[1])
            except IndexError:
                return set()
        return disallowed

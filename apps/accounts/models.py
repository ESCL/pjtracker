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

    def get_allowed_actions_for(self, obj):
        """
        Return a list of actions that can be executed by the user, which
        consist of a tuple with action name, and optionally a field name.
        """
        actions = []
        if not inspect.isclass(obj):
            obj = type(obj)

        for permcode in self.get_all_permissions():
            app, perm = permcode.split('.')
            action = perm.split('_', 2)
            model_name = action.pop(1)
            if model_name == obj._meta.model_name:
                actions.append(tuple(action))

        return actions

    def get_allowed_fields_for(self, obj):
        """
        Return a list of fields that can be modified by the user, based on the
        allowed actions.
        """
        fields = []
        for action in self.get_allowed_actions_for(obj):
            try:
                fields.append(action[1])
            except IndexError:
                return obj._meta.get_all_field_names()

        return fields


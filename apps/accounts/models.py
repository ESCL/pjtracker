import inspect

from django.contrib.auth.models import AbstractUser
from django.db import models

from django_signals_mixin import SignalsMixin
from .query import UserManager
from .utils import build_username


class Account(models.Model, SignalsMixin):

    name = models.CharField(
        max_length=128,
        help_text="Full name to identify the account."
    )
    code = models.CharField(
        max_length=16,
        unique=True,
        help_text="Short code used for users login."
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        return super(Account, self).save(*args, **kwargs)


class User(AbstractUser):

    owner = models.ForeignKey(
        'Account',
        null=True,
        blank=True,
        related_name='users'
    )

    objects = UserManager()

    @property
    def all_permissions(self):
        for g in self.groups.all():
            for p in g.permissions.all():
                yield p

    @property
    def domain(self):
        if self.is_staff or self.is_superuser:
            return None
        return self.owner

    @staticmethod
    def _classify(obj):
        """
        Return the class of the passed object (itself if it's a class).
        """
        if not inspect.isclass(obj):
            obj = type(obj)
        return obj

    def __str__(self):
        return '{} ({})'.format(self.username, self.get_full_name())

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
        # Start by assuming that all are disallowed
        disallowed = set(self._classify(obj)._meta.get_all_field_names())

        # Now if user has no domain or its domain matches obj owner allow
        # whatever actions determine
        if not self.domain or self.domain == obj.owner:
            for action in self.get_allowed_actions_for(obj):
                try:
                    disallowed.remove(action[1])
                except IndexError:
                    return set()

        # Return result
        return disallowed

    def save(self, *args, **kwargs):
        # Store normalized username (and ensure it's not empty)
        self.username = build_username(self.username, self.owner)
        if not self.username:
            raise ValueError("User 'username' cannot be empty.")

        # Return result of normal saves
        return super(User, self).save(*args, **kwargs)

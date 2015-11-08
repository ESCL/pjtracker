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

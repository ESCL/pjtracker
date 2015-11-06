__author__ = 'kako'

from django.db import models

from .query import OwnedEntityQuerySet


class OwnedEntity(models.Model):
    """
    Base class for all entities that are "owned" by an account.

    The field "owner" is nullable because we probably want "global" objects
    even for some ownable types (ie, locations).
    """
    class Meta:
        abstract = True

    objects = OwnedEntityQuerySet.as_manager()

    owner = models.ForeignKey(
        'accounts.Account',
        null=True,
        blank=True
    )


class History(models.Model):
    """
    Base class for all entities that store transitions, optimized to fetch
    values at specific date-times.
    """
    class Meta:
        abstract = True

    start = models.DateTimeField()
    end = models.DateTimeField()


class LabourType(object):

    MANAGERIAL = 'M'
    INDIRECT = 'I'
    DIRECT = 'D'

    TYPES = (('managerial', MANAGERIAL, 'MGT'),
             ('indirect', INDIRECT, 'IND'),
             ('direct', DIRECT, 'DIR'))
    CHOICES = ((t[1], t[0].title()) for t in TYPES)

    def __init__(self, name, value, code, allowed):
        self.name = name
        self.value = value
        self.code = code
        self.allowed = allowed

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name.title()

    def __hash__(self):
        return hash(self.value)


class AllowedLabourMixin(models.Model):
    """
    Provides three boolean fields for allowed labour classes and
    """
    class Meta:
        abstract = True

    managerial_labour = models.BooleanField(
        default=False
    )
    indirect_labour = models.BooleanField(
        default=False
    )
    direct_labour = models.BooleanField(
        default=False
    )

    @property
    def labour_types(self):
        l = []
        for name, value, code in LabourType.TYPES:
            allowed = getattr(self, '{}_labour'.format(name))
            l.append(LabourType(name, value, code, allowed))
        return l

    @property
    def allowed_labour_types(self):
        return {lt for lt in self.labour_types if lt.allowed}


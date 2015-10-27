from django.db import models

from ..common.db.models import OwnedEntity, History
from ..common.db.query import OwnedEntityQuerySet


class EquipmentType(OwnedEntity):

    name = models.CharField(
        max_length=128
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        related_name='subtypes'
    )

    def __str__(self):
        return self.name


class Resource(OwnedEntity):

    identifier = models.CharField(
        max_length=16,
    )
    company = models.ForeignKey(
        'organizations.Company'
    )
    team = models.ForeignKey(
        'organizations.Team'
    )
    project = models.ForeignKey(
        'work.Project'
    )
    location = models.ForeignKey(
        'geo.Location',
        null=True
    )
    space = models.ForeignKey(
        'geo.Space',
        null=True
    )
    resource_type = models.CharField(
        max_length=32,
    )

    @property
    def instance(self):
        return getattr(self, self.resource_type)

    def save(self, *args, **kwargs):
        self.resource_type = self.__class__._meta.model_name
        return super(Resource, self).save(*args, **kwargs)

    def __str__(self):
        return self.instance.__str__()


class Employee(Resource):

    objects = OwnedEntityQuerySet.as_manager()

    first_name = models.CharField(
        max_length=64
    )
    last_name = models.CharField(
        max_length=64
    )
    nation = models.ForeignKey(
        'geo.Nation'
    )
    birth_date = models.DateField(
        null=True, blank=True
    )
    photo = models.FileField(
        max_length=256, blank=True
    )
    home_address = models.CharField(
        max_length=256, null=True, blank=True
    )

    # Organizational data (required)
    position = models.ForeignKey(
        'organizations.Position'
    )

    @property
    def full_name(self):
        return '{}, {}'.format(self.last_name, self.first_name)

    @property
    def lodging(self):
        return self.space

    @property
    def nationality(self):
        return self.nation.demonym

    def __str__(self):
        return '{} ({})'.format(self.full_name, self.identifier)


class Equipment(Resource):

    class Meta:
        verbose_name_plural = 'equipment'

    type = models.ForeignKey(
        'EquipmentType'
    )

    @property
    def storage(self):
        return self.space

    def __str__(self):
        return '{} ({})'.format(self.type, self.identifier)


class ResourceHistory(History):

    class Meta:
        abstract = True


class LocationHistory(ResourceHistory):

    space = models.ForeignKey(
        'geo.Location'
    )


class SpaceHistory(ResourceHistory):

    space = models.ForeignKey(
        'geo.Space'
    )


class CompanyHistory(ResourceHistory):

    team = models.ForeignKey(
        'organizations.Company'
    )


class TeamHistory(ResourceHistory):

    team = models.ForeignKey(
        'organizations.Team'
    )


class ProjectHistory(ResourceHistory):

    team = models.ForeignKey(
        'work.Project'
    )


class PositionHistory(History):

    employee = models.ForeignKey(
        'Employee'
    )
    position = models.ForeignKey(
        'organizations.Position'
    )


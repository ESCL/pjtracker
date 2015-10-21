from django.db import models

from ..common.models import OwnedEntity, History


class Position(OwnedEntity):

    name = models.CharField(
        max_length=128
    )


class EquipmentType(OwnedEntity):

    name = models.CharField(
        max_length=128
    )


class Resource(OwnedEntity):

    identifier = models.CharField(
        max_length=16,
    )
    company = models.ForeignKey(
        'organizations.Company'
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


class Employee(Resource):

    first_name = models.CharField(
        max_length=64
    )
    last_name = models.CharField(
        max_length=64
    )
    nationality = models.ForeignKey(
        'locations.Nation'
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
        'Position'
    )

    @property
    def lodging(self):
        return self.space


class Equipment(Resource):

    type = models.ForeignKey(
        'EquipmentType'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        related_name='subtypes'
    )

    @property
    def storage(self):
        return self.space


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
        'Position'
    )


__author__ = 'kako'

from factory import DjangoModelFactory, Faker, SubFactory, post_generation

from ..geo.factories import LocationFactory
from .models import Project, Activity, ActivityGroup, ActivityGroupType


class ProjectFactory(DjangoModelFactory):

    class Meta:
        model = Project

    name = Faker('street_address')
    code = Faker('military_ship')
    location = SubFactory(LocationFactory)


class PhaseFactory(DjangoModelFactory):

    class Meta:
        model = ActivityGroupType

    name = 'Phase'


class DisciplineFactory(DjangoModelFactory):

    class Meta:
        model = ActivityGroupType

    name = 'Discipline'


class EngineeringFactory(DjangoModelFactory):

    class Meta:
        model = ActivityGroup

    name = 'Engineering'
    code = 'ENG'
    type = SubFactory(PhaseFactory)


class CivilWorksFactory(DjangoModelFactory):

    class Meta:
        model = ActivityGroup

    name = 'Civil'
    code = 'CIV'
    type = SubFactory(DisciplineFactory)


class ActivityFactory(DjangoModelFactory):

    class Meta:
        model = Activity

    name = 'Foundation 23 Design'
    code = 'FND23'
    project = SubFactory(ProjectFactory)

    @post_generation
    def groups(self, create, groups, **kwargs):
        if not create:
            return

        if not groups:
            groups = [EngineeringFactory.create(), CivilWorksFactory.create()]
        self.groups.add(*groups)

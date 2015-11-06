__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, LazyAttribute, Faker

from ..geo.factories import NationFactory, SpaceFactory
from ..organizations.factories import CompanyFactory, PositionFactory, TeamFactory
from ..work.factories import ProjectFactory
from .models import Employee, Equipment, EquipmentType


class EquipmentTypeFactory(DjangoModelFactory):

    class Meta:
        model = EquipmentType

    name = 'Excavator'


class EquipmentSubTypeFactory(DjangoModelFactory):

    class Meta:
        model = EquipmentType

    name = 'Backhoe'
    parent = SubFactory(EquipmentTypeFactory)


class EquipmentFactory(DjangoModelFactory):

    class Meta:
        model = Equipment

    identifier = Faker('ssn')
    company = SubFactory(CompanyFactory)
    team = SubFactory(TeamFactory)
    project = SubFactory(ProjectFactory)
    type = SubFactory(EquipmentSubTypeFactory)
    space = SubFactory(SpaceFactory)
    location = LazyAttribute(lambda obj: obj.space.location)


class EmployeeFactory(DjangoModelFactory):

    class Meta:
        model = Employee

    identifier = Faker('ssn')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    nation = SubFactory(NationFactory)
    company = LazyAttribute(lambda obj: obj.team.company)
    project = SubFactory(ProjectFactory)
    position = SubFactory(PositionFactory)
    space = SubFactory(SpaceFactory)
    location = LazyAttribute(lambda obj: obj.space.location)
    team = SubFactory(TeamFactory)

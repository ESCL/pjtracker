__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, LazyAttribute, Faker

from ..geo.factories import NationFactory, SpaceFactory
from ..organizations.factories import CompanyFactory
from ..work.factories import ProjectFactory
from .models import Employee, Position, Equipment, EquipmentType


class EquipmentTypeFactory(DjangoModelFactory):

    class Meta:
        model = EquipmentType

    name = 'excavator'


class EquipmentSubTypeFactory(DjangoModelFactory):

    class Meta:
        model = EquipmentType

    name = 'excavator'
    parent = SubFactory(EquipmentTypeFactory)


class EquipmentFactory(DjangoModelFactory):

    class Meta:
        model = Equipment

    identifier = Faker('ssn')
    company = SubFactory(CompanyFactory)
    project = SubFactory(ProjectFactory)
    type = SubFactory(EquipmentSubTypeFactory)
    space = SubFactory(SpaceFactory)
    location = LazyAttribute(lambda obj: obj.space.location)


class PositionFactory(DjangoModelFactory):

    class Meta:
        model = Position

    name = Faker('job')


class EmployeeFactory(DjangoModelFactory):

    class Meta:
        model = Employee

    identifier = Faker('ssn')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    nation = SubFactory(NationFactory)
    company = SubFactory(CompanyFactory)
    project = SubFactory(ProjectFactory)
    position = SubFactory(PositionFactory)
    space = SubFactory(SpaceFactory)
    location = LazyAttribute(lambda obj: obj.space.location)



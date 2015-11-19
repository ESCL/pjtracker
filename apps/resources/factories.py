__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, LazyAttribute, Faker, post_generation

from ..organizations.factories import PositionFactory, TeamFactory
from ..work.factories import ProjectFactory
from .models import Employee, Equipment, EquipmentType


class EquipmentTypeFactory(DjangoModelFactory):

    class Meta:
        model = EquipmentType

    name = 'Earthworks'


class EquipmentSubTypeFactory(DjangoModelFactory):

    class Meta:
        model = EquipmentType

    name = 'Backhoe'
    parent = SubFactory(EquipmentTypeFactory)


class EquipmentFactory(DjangoModelFactory):

    class Meta:
        model = Equipment

    owner = LazyAttribute(lambda obj: obj.team.owner)
    identifier = Faker('ssn')
    model = 'Komatsu WB140'
    year = 2005
    company = LazyAttribute(lambda obj: obj.team.company)
    team = SubFactory(TeamFactory)
    project = SubFactory(ProjectFactory)
    type = SubFactory(EquipmentSubTypeFactory)


class EmployeeFactory(DjangoModelFactory):

    class Meta:
        model = Employee

    owner = LazyAttribute(lambda obj: obj.team.owner)
    identifier = Faker('ssn')
    first_name = Faker('first_name_male')
    last_name = Faker('last_name')
    gender = 'M'
    company = LazyAttribute(lambda obj: obj.team.company)
    project = SubFactory(ProjectFactory)
    position = SubFactory(PositionFactory)
    team = SubFactory(TeamFactory)

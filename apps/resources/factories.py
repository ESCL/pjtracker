__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, LazyAttribute, Faker

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

    owner = LazyAttribute(lambda obj: obj.team.owner)
    identifier = Faker('ssn')
    company = LazyAttribute(lambda obj: obj.team.company)
    team = SubFactory(TeamFactory)
    project = SubFactory(ProjectFactory)
    type = SubFactory(EquipmentSubTypeFactory)


class EmployeeFactory(DjangoModelFactory):

    class Meta:
        model = Employee

    owner = LazyAttribute(lambda obj: obj.team.owner)
    identifier = Faker('ssn')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    company = LazyAttribute(lambda obj: obj.team.company)
    project = SubFactory(ProjectFactory)
    position = SubFactory(PositionFactory)
    team = SubFactory(TeamFactory)

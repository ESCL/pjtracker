__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, LazyAttribute, Faker

from ..accounts.factories import AccountBaseFactory
from ..organizations.factories import CompanyBaseFactory, PositionFactory, PositionBaseFactory, TeamFactory
from ..work.factories import ProjectFactory, ProjectBaseFactory
from .models import Employee, Equipment, EquipmentType


# Base factories
# These generate no fake data, they are used for imports and as base classes

class EquipmentTypeBaseFactory(DjangoModelFactory):

    class Meta:
        model = EquipmentType


class EmployeeBaseFactory(DjangoModelFactory):

    class Meta:
        model = Employee

    owner = SubFactory(AccountBaseFactory)
    position = SubFactory(PositionBaseFactory)
    company = SubFactory(CompanyBaseFactory)
    project = SubFactory(ProjectBaseFactory)


class EquipmentBaseFactory(DjangoModelFactory):

    class Meta:
        model = Equipment

    owner = SubFactory(AccountBaseFactory)
    company = SubFactory(CompanyBaseFactory)
    type = SubFactory(EquipmentTypeBaseFactory)
    project = SubFactory(ProjectBaseFactory)


# Smart factories
# These produce fake data, used in unit tests and to bootstrap dev dbs

class EquipmentTypeFactory(EquipmentTypeBaseFactory):

    name = 'Earthworks'


class EquipmentSubTypeFactory(EquipmentTypeBaseFactory):

    name = 'Backhoe'
    parent = SubFactory(EquipmentTypeFactory)


class EquipmentFactory(EquipmentBaseFactory):

    owner = LazyAttribute(lambda obj: obj.team.owner)
    identifier = Faker('ssn')
    model = 'Komatsu WB140'
    year = 2005
    company = LazyAttribute(lambda obj: obj.team.company)
    team = SubFactory(TeamFactory)
    project = SubFactory(ProjectFactory)
    type = SubFactory(EquipmentSubTypeFactory)


class EmployeeFactory(EmployeeBaseFactory):

    owner = LazyAttribute(lambda obj: obj.team.owner)
    identifier = Faker('ssn')
    first_name = Faker('first_name_male')
    last_name = Faker('last_name')
    gender = 'M'
    company = LazyAttribute(lambda obj: obj.team.company)
    project = SubFactory(ProjectFactory)
    position = SubFactory(PositionFactory)
    team = SubFactory(TeamFactory)


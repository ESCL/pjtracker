__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, Faker, SelfAttribute

from ..common.factories import NullableSubFactory
from ..accounts.factories import AccountBaseFactory, AccountFactory
from ..geo.factories import LocationBaseFactory, LocationFactory
from ..organizations.factories import (
    CompanyBaseFactory, CompanyFactory, DepartmentBaseFactory,
    DepartmentFactory, PositionFactory, PositionBaseFactory, TeamFactory
)
from ..work.factories import ProjectBaseFactory, ProjectFactory
from .models import Employee, Equipment, EquipmentType


# Base factories
# These generate no fake data, they are used for imports and as base classes

class EquipmentTypeBaseFactory(DjangoModelFactory):

    class Meta:
        model = EquipmentType
        django_get_or_create = ('owner', 'code',)

    owner = SubFactory(AccountBaseFactory)


class EmployeeBaseFactory(DjangoModelFactory):

    class Meta:
        model = Employee
        django_get_or_create = ('owner', 'identifier',)

    owner = SubFactory(AccountBaseFactory)
    company = SubFactory(CompanyBaseFactory, owner=SelfAttribute('..owner'))
    position = SubFactory(PositionBaseFactory, owner=SelfAttribute('..owner'))
    department = NullableSubFactory(DepartmentBaseFactory, owner=SelfAttribute('..owner'))
    project = NullableSubFactory(ProjectBaseFactory, owner=SelfAttribute('..owner'))
    location = NullableSubFactory(LocationBaseFactory, owner=SelfAttribute('..owner'))


class EquipmentBaseFactory(DjangoModelFactory):

    class Meta:
        model = Equipment
        django_get_or_create = ('owner', 'identifier',)

    owner = SubFactory(AccountBaseFactory)
    company = SubFactory(CompanyBaseFactory, owner=SelfAttribute('..owner'))
    type = SubFactory(EquipmentTypeBaseFactory, owner=SelfAttribute('..owner'))
    project = NullableSubFactory(ProjectBaseFactory, owner=SelfAttribute('..owner'))
    location = NullableSubFactory(LocationBaseFactory, owner=SelfAttribute('..owner'))


# Smart factories
# These produce fake data, used in unit tests and to bootstrap dev dbs

class EquipmentTypeFactory(DjangoModelFactory):

    class Meta:
        model = EquipmentType

    name = 'Earthworks'
    code = 'EAR'


class EquipmentSubTypeFactory(EquipmentTypeFactory):

    name = 'Backhoe'
    code = 'BKH'
    parent = SubFactory(EquipmentTypeFactory)


class EquipmentFactory(DjangoModelFactory):

    class Meta:
        model = Equipment

    owner = SubFactory(AccountFactory)
    identifier = Faker('ssn')
    model = 'Komatsu WB140'
    year = 2005
    company = SubFactory(CompanyFactory, owner=SelfAttribute('..owner'))
    project = SubFactory(ProjectFactory, owner=SelfAttribute('..owner'))
    type = SubFactory(EquipmentSubTypeFactory, owner=SelfAttribute('..owner'))
    team = SubFactory(TeamFactory, owner=SelfAttribute('..owner'),
                      company=SelfAttribute('..company'))
    location = SubFactory(LocationFactory, owner=SelfAttribute('..owner'))


class EmployeeFactory(DjangoModelFactory):

    class Meta:
        model = Employee

    owner = SubFactory(AccountFactory)
    identifier = Faker('ssn')
    first_name = Faker('first_name_male')
    last_name = Faker('last_name')
    gender = 'M'
    company = SubFactory(CompanyFactory, owner=SelfAttribute('..owner'))
    department = SubFactory(DepartmentFactory, owner=SelfAttribute('..owner'))
    project = SubFactory(ProjectFactory, owner=SelfAttribute('..owner'))
    position = SubFactory(PositionFactory, owner=SelfAttribute('..owner'))
    team = SubFactory(TeamFactory, owner=SelfAttribute('..owner'),
                      company=SelfAttribute('..company'))
    location = SubFactory(LocationFactory, owner=SelfAttribute('..owner'))


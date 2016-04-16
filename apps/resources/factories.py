__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, Faker, SelfAttribute, LazyAttribute

from ..common.factories import NullableSubFactory
from ..accounts.factories import AccountBaseFactory, AccountFactory
from ..geo.factories import LocationBaseFactory, LocationFactory
from ..organizations.factories import (
    CompanyBaseFactory, CompanyFactory, DepartmentBaseFactory,
    DepartmentFactory, PositionFactory, PositionBaseFactory, TeamFactory,
)
from ..work.factories import ProjectBaseFactory, ProjectFactory
from .models import Employee, Equipment, EquipmentType, ResourceCategory


# Base factories
# These generate no fake data, they are used for imports and as base classes

class EquipmentTypeFactory(DjangoModelFactory):

    class Meta:
        model = EquipmentType
        django_get_or_create = ('owner', 'code',)

    owner = SubFactory(AccountBaseFactory)


class ResourceCategoryFactory(DjangoModelFactory):

    class Meta:
        model = ResourceCategory
        django_get_or_create = ('owner', 'name',)

    owner = SubFactory(AccountFactory)
    resource_type = 'all'


class EmployeeFactory(DjangoModelFactory):

    class Meta:
        model = Employee
        django_get_or_create = ('owner', 'identifier',)

    owner = SubFactory(AccountBaseFactory)
    company = SubFactory(CompanyBaseFactory, owner=SelfAttribute('..owner'))
    department = NullableSubFactory(DepartmentBaseFactory, owner=SelfAttribute('..owner'))
    position = SubFactory(PositionBaseFactory, owner=SelfAttribute('..owner'))
    category = NullableSubFactory(ResourceCategoryFactory, owner=SelfAttribute('..owner'))
    project = NullableSubFactory(ProjectBaseFactory, owner=SelfAttribute('..owner'))
    location = NullableSubFactory(LocationBaseFactory, owner=SelfAttribute('..owner'))


class EquipmentFactory(DjangoModelFactory):

    class Meta:
        model = Equipment
        django_get_or_create = ('owner', 'identifier',)

    owner = SubFactory(AccountBaseFactory)
    company = SubFactory(CompanyBaseFactory, owner=SelfAttribute('..owner'))
    type = SubFactory(EquipmentTypeFactory, owner=SelfAttribute('..owner'))
    category = NullableSubFactory(ResourceCategoryFactory, owner=SelfAttribute('..owner'))
    project = NullableSubFactory(ProjectBaseFactory, owner=SelfAttribute('..owner'))
    location = NullableSubFactory(LocationBaseFactory, owner=SelfAttribute('..owner'))


# Fake factories
# These produce fake data, used in unit tests and to bootstrap dev dbs

class EquipmentTypeFakeFactory(DjangoModelFactory):

    class Meta:
        model = EquipmentType

    name = 'Earthworks'
    code = 'EAR'


class EquipmentSubTypeFakeFactory(EquipmentTypeFakeFactory):

    name = 'Backhoe'
    code = 'BKH'
    parent = SubFactory(EquipmentTypeFakeFactory)


class ResourceCategoryFakeFactory(ResourceCategoryFactory):

    owner = SubFactory(AccountFactory)
    name = Faker('random_element', elements=('Senior', 'Semi-Senior', 'Junior'))
    code = LazyAttribute(lambda obj: obj.name[:2].upper())
    resource_type = 'employee'


class EquipmentFakeFactory(DjangoModelFactory):

    class Meta:
        model = Equipment

    owner = SubFactory(AccountFactory)
    identifier = Faker('ssn')
    model = 'Komatsu WB140'
    year = 2005
    company = SubFactory(CompanyFactory, owner=SelfAttribute('..owner'))
    type = SubFactory(EquipmentSubTypeFakeFactory, owner=SelfAttribute('..owner'))
    category = SubFactory(ResourceCategoryFakeFactory, owner=SelfAttribute('..owner'))
    project = SubFactory(ProjectFactory, owner=SelfAttribute('..owner'))
    team = SubFactory(TeamFactory, owner=SelfAttribute('..owner'),
                      company=SelfAttribute('..company'))
    location = SubFactory(LocationFactory, owner=SelfAttribute('..owner'))


class EmployeeFakeFactory(DjangoModelFactory):

    class Meta:
        model = Employee

    owner = SubFactory(AccountFactory)
    identifier = Faker('ssn')
    first_name = Faker('first_name_male')
    last_name = Faker('last_name')
    gender = 'M'
    company = SubFactory(CompanyFactory, owner=SelfAttribute('..owner'))
    department = SubFactory(DepartmentFactory, owner=SelfAttribute('..owner'))
    position = SubFactory(PositionFactory, owner=SelfAttribute('..owner'))
    category = SubFactory(ResourceCategoryFakeFactory, owner=SelfAttribute('..owner'))
    project = SubFactory(ProjectFactory, owner=SelfAttribute('..owner'))
    team = SubFactory(TeamFactory, owner=SelfAttribute('..owner'),
                      company=SelfAttribute('..company'))
    location = SubFactory(LocationFactory, owner=SelfAttribute('..owner'))

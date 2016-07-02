__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, Faker, SelfAttribute, LazyAttribute

from ..common.factories import NullableSubFactory
from ..common.utils import generate_unique_code
from ..accounts.factories import AccountFactory, AccountFakeFactory
from ..geo.factories import LocationFactory, LocationFakeFactory
from ..organizations.factories import (
    CompanyFactory, CompanyFakeFactory, DepartmentFactory,
    DepartmentFakeFactory, PositionFakeFactory, PositionFactory, TeamFakeFactory,
)
from ..work.factories import ProjectFactory
from .models import Employee, Equipment, EquipmentType, ResourceCategory


# Base factories
# These generate no fake data, they are used for imports and as base classes

class EquipmentTypeFactory(DjangoModelFactory):

    class Meta:
        model = EquipmentType
        django_get_or_create = ('owner', 'code',)

    owner = SubFactory(AccountFactory)


class ResourceCategoryFactory(DjangoModelFactory):

    class Meta:
        model = ResourceCategory
        django_get_or_create = ('owner', 'code',)

    owner = SubFactory(AccountFactory)
    resource_type = 'all'


class EmployeeFactory(DjangoModelFactory):

    class Meta:
        model = Employee
        django_get_or_create = ('owner', 'identifier',)

    owner = SubFactory(AccountFactory)
    company = SubFactory(CompanyFactory, owner=SelfAttribute('..owner'))
    department = NullableSubFactory(DepartmentFactory, owner=SelfAttribute('..owner'))
    position = SubFactory(PositionFactory, owner=SelfAttribute('..owner'))
    category = NullableSubFactory(ResourceCategoryFactory, owner=SelfAttribute('..owner'))
    project = NullableSubFactory(ProjectFactory, owner=SelfAttribute('..owner'))
    location = NullableSubFactory(LocationFactory, owner=SelfAttribute('..owner'))


class EquipmentFactory(DjangoModelFactory):

    class Meta:
        model = Equipment
        django_get_or_create = ('owner', 'identifier',)

    owner = SubFactory(AccountFactory)
    company = SubFactory(CompanyFactory, owner=SelfAttribute('..owner'))
    type = SubFactory(EquipmentTypeFactory, owner=SelfAttribute('..owner'))
    category = NullableSubFactory(ResourceCategoryFactory, owner=SelfAttribute('..owner'))
    project = NullableSubFactory(ProjectFactory, owner=SelfAttribute('..owner'))
    location = NullableSubFactory(LocationFactory, owner=SelfAttribute('..owner'))


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

    owner = SubFactory(AccountFakeFactory)
    name = Faker('random_element', elements=('Senior', 'Semi-Senior', 'Junior'))
    code = LazyAttribute(lambda obj: generate_unique_code(obj, 'code', 'name', min_len=2, max_len=3))
    resource_type = 'all'


class EquipmentFakeFactory(DjangoModelFactory):

    class Meta:
        model = Equipment

    owner = SubFactory(AccountFakeFactory)
    identifier = Faker('ssn')
    model = 'Komatsu WB140'
    year = 2005
    company = SubFactory(CompanyFakeFactory, owner=SelfAttribute('..owner'))
    type = SubFactory(EquipmentSubTypeFakeFactory, owner=SelfAttribute('..owner'))
    category = SubFactory(ResourceCategoryFakeFactory, owner=SelfAttribute('..owner'))
    team = SubFactory(TeamFakeFactory, owner=SelfAttribute('..owner'),
                      company=SelfAttribute('..company'))
    location = SubFactory(LocationFakeFactory, owner=SelfAttribute('..owner'))


class EmployeeFakeFactory(DjangoModelFactory):

    class Meta:
        model = Employee

    owner = SubFactory(AccountFakeFactory)
    identifier = Faker('ssn')
    first_name = Faker('first_name_male')
    last_name = Faker('last_name')
    gender = 'M'
    company = SubFactory(CompanyFakeFactory, owner=SelfAttribute('..owner'))
    department = SubFactory(DepartmentFakeFactory, owner=SelfAttribute('..owner'))
    position = SubFactory(PositionFakeFactory, owner=SelfAttribute('..owner'))
    category = SubFactory(ResourceCategoryFakeFactory, owner=SelfAttribute('..owner'))
    team = SubFactory(TeamFakeFactory, owner=SelfAttribute('..owner'),
                      company=SelfAttribute('..company'))
    location = SubFactory(LocationFakeFactory, owner=SelfAttribute('..owner'))

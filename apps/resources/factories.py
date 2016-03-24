__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, LazyAttribute, Faker, SelfAttribute, PostGeneration

from ..accounts.factories import AccountBaseFactory
from ..organizations.factories import CompanyBaseFactory, PositionFactory, PositionBaseFactory, TeamFactory
from ..work.factories import ProjectFactory, set_subfactory_project
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
    project = PostGeneration(set_subfactory_project)


class EquipmentBaseFactory(DjangoModelFactory):

    class Meta:
        model = Equipment
        django_get_or_create = ('owner', 'identifier',)

    owner = SubFactory(AccountBaseFactory)
    company = SubFactory(CompanyBaseFactory, owner=SelfAttribute('..owner'))
    type = SubFactory(EquipmentTypeBaseFactory, owner=SelfAttribute('..owner'))
    project = PostGeneration(set_subfactory_project)


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


__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, Faker, post_generation, LazyAttribute, SelfAttribute

from ..accounts.factories import AccountFakeFactory, AccountFactory
from ..common.utils import generate_code_from_name
from .models import Company, Department, Team, Position


# Base factories
# These generate no fake data, they are used for imports and as base classes

class CompanyFactory(DjangoModelFactory):

    class Meta:
        model = Company
        django_get_or_create = ('owner', 'code',)

    owner = SubFactory(AccountFactory)


class DepartmentFactory(DjangoModelFactory):

    class Meta:
        model = Department
        django_get_or_create = ('owner', 'code',)

    owner = SubFactory(AccountFactory)


class PositionFactory(DjangoModelFactory):

    class Meta:
        model = Position
        django_get_or_create = ('owner', 'code',)

    owner = SubFactory(AccountFactory)


# Smart factories
# These produce fake data, used in unit tests and to bootstrap dev dbs

class CompanyFakeFactory(CompanyFactory):

    owner = SubFactory(AccountFakeFactory)
    name = Faker('company')
    code = LazyAttribute(lambda obj: generate_code_from_name(obj.name))


class DepartmentFakeFactory(DepartmentFactory):

    owner = SubFactory(AccountFakeFactory)
    name = Faker('color_name')
    code = LazyAttribute(lambda obj: generate_code_from_name(obj.name))


class PositionFakeFactory(PositionFactory):

    owner = None
    name = Faker('job')
    code = LazyAttribute(lambda obj: generate_code_from_name(obj.name))


class TeamFakeFactory(DjangoModelFactory):

    class Meta:
        model = Team

    owner = SubFactory(AccountFakeFactory)
    name = Faker('sentence', nb_words=2)
    code = LazyAttribute(lambda obj: generate_code_from_name(obj.name))
    company = SubFactory(CompanyFakeFactory, owner=SelfAttribute('..owner'))

    @post_generation
    def timekeepers(self, create, values):
        if create and values:
            self.timekeepers.add(*values)

    @post_generation
    def supervisors(self, create, values):
        if create and values:
            self.supervisors.add(*values)

    @post_generation
    def activities(self, create, values):
        if create and values:
            self.activities.add(*values)

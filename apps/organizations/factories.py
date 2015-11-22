__author__ = 'kako'

import re

from factory import DjangoModelFactory, SubFactory, Faker, post_generation, LazyAttribute

from ..accounts.factories import AccountFactory
from ..common.utils import generate_code_from_name
from .models import Company, Team, Position


class CompanyFactory(DjangoModelFactory):

    class Meta:
        model = Company

    owner = SubFactory(AccountFactory)
    name = Faker('company')
    code = LazyAttribute(lambda obj: generate_code_from_name(obj.name))


class TeamFactory(DjangoModelFactory):

    class Meta:
        model = Team

    owner = LazyAttribute(lambda obj: obj.company.owner)
    name = Faker('sentence', nb_words=2)
    code = LazyAttribute(lambda obj: generate_code_from_name(obj.name))
    company = SubFactory(CompanyFactory)

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


class PositionFactory(DjangoModelFactory):

    class Meta:
        model = Position
        django_get_or_create = ('name',)

    name = Faker('job')
    code = LazyAttribute(lambda obj: generate_code_from_name(obj.name))


__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, Faker, post_generation, LazyAttribute

from ..accounts.factories import AccountFactory
from .models import Company, Team, Position


class CompanyFactory(DjangoModelFactory):

    class Meta:
        model = Company

    owner = SubFactory(AccountFactory)
    name = Faker('company')
    code = Faker('word')


class TeamFactory(DjangoModelFactory):

    class Meta:
        model = Team

    owner = LazyAttribute(lambda obj: obj.company.owner)
    name = Faker('sentence', nb_words=2)
    code = Faker('word')
    company = SubFactory(CompanyFactory)

    @post_generation
    def timekeepers(self, create, values):
        if create and values:
            self.timekeepers.add(*values)

    @post_generation
    def supervisors(self, create, values):
        if create and values:
            self.supervisors.add(*values)


class PositionFactory(DjangoModelFactory):

    class Meta:
        model = Position

    name = Faker('job')

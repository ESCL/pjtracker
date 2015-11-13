__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, Faker, post_generation, LazyAttribute

from ..accounts.factories import AccountFactory
from .models import Company, Team, Position


class CompanyFactory(DjangoModelFactory):

    class Meta:
        model = Company

    owner = SubFactory(AccountFactory)
    name = Faker('company')
    code = LazyAttribute(lambda obj: ''.join(x[0] for x in obj.name.split()).upper())


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

    @post_generation
    def activities(self, create, values):
        if create and values:
            self.activities.add(*values)


class PositionFactory(DjangoModelFactory):

    class Meta:
        model = Position

    name = Faker('job')
    code = LazyAttribute(lambda obj: obj.name[:3].upper())


__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, Faker

from .models import Company, Team, Position


class CompanyFactory(DjangoModelFactory):

    class Meta:
        model = Company

    name = Faker('company')
    code = Faker('word')


class TeamFactory(DjangoModelFactory):

    class Meta:
        model = Team

    name = Faker('sentence', nb_words=2)
    code = Faker('word')
    company = SubFactory(CompanyFactory)


class PositionFactory(DjangoModelFactory):

    class Meta:
        model = Position

    name = Faker('job')

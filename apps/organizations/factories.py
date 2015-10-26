__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, Faker

from .models import Company, Team, Position


class CompanyFactory(DjangoModelFactory):

    class Meta:
        model = Company

    name = Faker('company')
    code = 'CPY'


class TeamFactory(DjangoModelFactory):

    class Meta:
        model = Team

    name = 'Engineering'
    code = 'ENG'
    company = SubFactory(CompanyFactory)


class PositionFactory(DjangoModelFactory):

    class Meta:
        model = Position

    name = Faker('job')

__author__ = 'kako'

from factory import SubFactory, LazyAttribute, Faker
from factory.django import DjangoModelFactory

from ...geo.tests.factories import NationFactory, SpaceFactory
from ...organizations.tests.factories import CompanyFactory
from ...work.tests.factories import ProjectFactory
from ..models import Employee, Position


class PositionFactory(DjangoModelFactory):

    class Meta:
        model = Position

    name = Faker('job')


class EmployeeFactory(DjangoModelFactory):

    class Meta:
        model = Employee

    identifier = Faker('ssn')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    nationality = SubFactory(NationFactory)
    company = SubFactory(CompanyFactory)
    project = SubFactory(ProjectFactory)
    position = SubFactory(PositionFactory)
    space = SubFactory(SpaceFactory)
    location = LazyAttribute(lambda obj: obj.space.location)



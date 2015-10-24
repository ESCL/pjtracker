__author__ = 'kako'

from factory import DjangoModelFactory, Faker, SubFactory

from ...geo.tests.factories import LocationFactory
from ..models import Project


class ProjectFactory(DjangoModelFactory):

    class Meta:
        model = Project

    name = Faker('street_address')
    code = Faker('military_ship')
    location = SubFactory(LocationFactory)

__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, Faker

from ..accounts.factories import AccountBaseFactory, AccountFactory
from .models import Location


# Base factories
# These generate no fake data, they are used for imports and as base classes

class LocationBaseFactory(DjangoModelFactory):

    class Meta:
        model = Location
        django_get_or_create = ('owner', 'name',)

    owner = SubFactory(AccountBaseFactory)


# Smart factories
# These produce fake data, used in unit tests and to bootstrap dev dbs

class LocationFactory(LocationBaseFactory):

    owner = SubFactory(AccountFactory)
    name = Faker('street_address')
    latitude = Faker('latitude')
    longitude = Faker('longitude')

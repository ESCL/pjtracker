__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, Faker

from ..accounts.factories import AccountFactory, AccountFakeFactory
from .models import Location


# Base factories
# These generate no fake data, they are used for imports and as base classes

class LocationFactory(DjangoModelFactory):

    class Meta:
        model = Location
        django_get_or_create = ('owner', 'name',)

    owner = SubFactory(AccountFactory)


# Smart factories
# These produce fake data, used in unit tests and to bootstrap dev dbs

class LocationFakeFactory(LocationFactory):

    owner = SubFactory(AccountFakeFactory)
    name = Faker('street_address')
    latitude = Faker('latitude')
    longitude = Faker('longitude')

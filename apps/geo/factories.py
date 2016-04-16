__author__ = 'kako'

from factory import DjangoModelFactory, Faker
from .models import Location


class LocationFactory(DjangoModelFactory):

    class Meta:
        model = Location

    name = Faker('street_address')
    latitude = Faker('latitude')
    longitude = Faker('longitude')

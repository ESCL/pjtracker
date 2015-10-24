__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, Faker, LazyAttribute

from ..models import Nation, Region, Locality, Location, Space


class NationFactory(DjangoModelFactory):

    class Meta:
        model = Nation

    name = Faker('country')
    code = Faker('country_code')
    demonym = LazyAttribute(lambda obj: '{}an'.format(obj.name))


class RegionFactory(DjangoModelFactory):

    class Meta:
        model = Region

    name = Faker('state')
    code = 'XX'
    nation = SubFactory(NationFactory)


class LocalityFactory(DjangoModelFactory):

    class Meta:
        model = Locality

    name = Faker('city')
    region = SubFactory(RegionFactory)


class LocationFactory(DjangoModelFactory):

    class Meta:
        model = Location

    address = Faker('street_address')
    locality = SubFactory(LocalityFactory)
    latitude = Faker('latitude')
    longitude = Faker('longitude')


class SpaceFactory(DjangoModelFactory):

    class Meta:
        model = Space

    location = SubFactory(LocationFactory)
    section = Faker('random_letter')
    identifier = Faker('secondary_address')

__author__ = 'kako'

from factory import DjangoModelFactory, Faker, SubFactory, LazyAttribute

from .models import Account, User


class AccountFactory(DjangoModelFactory):

    class Meta:
        model = Account

    name = Faker('company')


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    first_name = Faker('first_name')
    username = LazyAttribute(lambda obj: obj.first_name.lower())
    owner = SubFactory(AccountFactory)

__author__ = 'kako'

from django.contrib.auth.models import User
from factory import DjangoModelFactory, Faker, SubFactory, RelatedFactory, LazyAttribute

from .models import Account, UserProfile


class AccountFactory(DjangoModelFactory):

    class Meta:
        model = Account


class UserProfileFactory(DjangoModelFactory):

    class Meta:
        model = UserProfile

    account = SubFactory(AccountFactory)


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    first_name = Faker('first_name')
    username = LazyAttribute(lambda obj: obj.first_name.lower())
    profile = RelatedFactory(UserProfileFactory, 'user', user=None)

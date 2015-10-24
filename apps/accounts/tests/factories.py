__author__ = 'kako'

from django.contrib.auth.models import User

from factory import SubFactory, RelatedFactory
from factory.django import DjangoModelFactory

from ..models import Account, UserProfile


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

    profile = RelatedFactory(UserProfileFactory, 'user', user=None)

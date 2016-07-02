__author__ = 'kako'

from factory import DjangoModelFactory, Faker, SubFactory, LazyAttribute, post_generation

from ..common.utils import generate_unique_code
from .models import Account, User


# Base factories
# These generate no fake data, they are used for imports and as base classes

class AccountFactory(DjangoModelFactory):

    class Meta:
        model = Account
        django_get_or_create = ('code',)


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('owner', 'username',)

    owner = SubFactory(AccountFactory)


# Smart factories
# These produce fake data, used in unit tests and to bootstrap dev dbs

class AccountFakeFactory(AccountFactory):

    name = Faker('company')
    code = LazyAttribute(lambda obj: generate_unique_code(obj, 'code', 'name', min_len=3, max_len=6))


class UserFakeFactory(UserFactory):

    owner = SubFactory(AccountFakeFactory)
    username = Faker('user_name')
    first_name = Faker('first_name')
    password = '123'

    @post_generation
    def groups(self, created, value):
        if created and value:
            self.groups.add(*value)

    @post_generation
    def user_permissions(self, created, value):
        if created and value:
            self.user_permissions.add(*value)

    @classmethod
    def create(cls, **kwargs):
        user = super(UserFakeFactory, cls).create(**kwargs)
        user.set_password(user.password)
        user.save()
        return user

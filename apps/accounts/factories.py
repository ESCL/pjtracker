__author__ = 'kako'

from factory import DjangoModelFactory, Faker, SubFactory, LazyAttribute, post_generation, PostGeneration

from ..common.utils import generate_code_from_name
from .models import Account, User


# Base factories
# These generate no fake data, they are used for imports and as base classes

class AccountBaseFactory(DjangoModelFactory):

    class Meta:
        model = Account
        django_get_or_create = ('code',)


class UserBaseFactory(DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('owner', 'username',)

    owner = SubFactory(AccountBaseFactory)


# Smart factories
# These produce fake data, used in unit tests and to bootstrap dev dbs

class AccountFactory(DjangoModelFactory):

    class Meta:
        model = Account

    name = Faker('company')
    code = LazyAttribute(lambda obj: generate_code_from_name(obj.name))


class UserFactory(UserBaseFactory):

    owner = SubFactory(AccountFactory)
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
        user = super(UserFactory, cls).create(**kwargs)
        user.set_password(user.password)
        user.save()
        return user

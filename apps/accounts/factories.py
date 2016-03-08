__author__ = 'kako'

from factory import DjangoModelFactory, Faker, SubFactory, LazyAttribute, post_generation

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

class AccountFactory(AccountBaseFactory):

    name = Faker('company')
    code = LazyAttribute(lambda obj: generate_code_from_name(obj.name))


class UserFactory(UserBaseFactory):

    owner = SubFactory(AccountFactory)
    username = LazyAttribute(lambda obj: obj.first_name.lower())
    first_name = Faker('first_name')

    @post_generation
    def groups(self, created, value):
        if created and value:
            self.groups.add(*value)

    @post_generation
    def password(self, created, value):
        if created and value:
            self.set_password(value)
            self.save()

    @post_generation
    def user_permissions(self, created, value):
        if created and value:
            self.user_permissions.add(*value)
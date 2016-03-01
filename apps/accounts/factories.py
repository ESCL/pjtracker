__author__ = 'kako'

from factory import DjangoModelFactory, Faker, SubFactory, LazyAttribute, post_generation

from ..common.utils import generate_code_from_name
from .models import Account, User


class AccountFactory(DjangoModelFactory):

    class Meta:
        model = Account
        django_get_or_create = ('code',)

    name = Faker('company')
    code = LazyAttribute(lambda obj: generate_code_from_name(obj.name))


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

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
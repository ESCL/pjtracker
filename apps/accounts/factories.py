__author__ = 'kako'

from factory import DjangoModelFactory, Faker, SubFactory, LazyAttribute, post_generation

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

    @post_generation
    def groups(self, created, value):
        if created and value:
            self.groups.add(*value)

    @post_generation
    def password(self, created, value):
        if created and value:
            self.set_password(value)
            self.save()

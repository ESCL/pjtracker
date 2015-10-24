__author__ = 'kako'

from django.contrib.auth.models import User

from factory import SubFactory, RelatedFactory, Faker
from factory.django import DjangoModelFactory

from ..models import Company


class CompanyFactory(DjangoModelFactory):

    class Meta:
        model = Company

    name = Faker('company')
    code = 'CPY'

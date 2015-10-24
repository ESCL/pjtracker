__author__ = 'kako'

from factory import DjangoModelFactory, Faker

from .models import Company


class CompanyFactory(DjangoModelFactory):

    class Meta:
        model = Company

    name = Faker('company')
    code = 'CPY'

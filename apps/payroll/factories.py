__author__ = 'kako'

from .models import HourType

from factory import DjangoModelFactory


class HourTypeFactory(DjangoModelFactory):

    class Meta:
        model = HourType
        django_get_or_create = ('owner', 'code', )


class NormalHoursFactory(HourTypeFactory):
    name = 'Standard'
    code = 'STD'


class Overtime150HoursFactory(HourTypeFactory):
    name = 'Overtime 150%'
    code = 'OT150'


class Overtime200HoursFactory(HourTypeFactory):
    name = 'Overtime 200%'
    code = 'OT200'

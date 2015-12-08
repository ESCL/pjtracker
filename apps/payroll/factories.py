__author__ = 'kako'

from .models import HourType

from factory import DjangoModelFactory


class NormalHoursFactory(DjangoModelFactory):

    class Meta:
        model = HourType

    name = 'Normal'
    code = 'N'


class Overtime150HoursFactory(DjangoModelFactory):

    class Meta:
        model = HourType

    name = 'Overtime 150%'
    code = 'OT150'


class Overtime200HoursFactory(DjangoModelFactory):

    class Meta:
        model = HourType

    name = 'Overtime 200%'
    code = 'OT200'

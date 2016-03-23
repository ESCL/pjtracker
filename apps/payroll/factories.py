__author__ = 'kako'

from datetime import datetime, timedelta

from factory import DjangoModelFactory, LazyAttribute

from .models import HourType, Period



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


class PeriodFactory(DjangoModelFactory):

    class Meta:
        model = Period

    start_date = LazyAttribute(lambda obj: datetime.utcnow().date())
    end_date = LazyAttribute(lambda obj: obj.start_date + timedelta(days=30))
    forecast_start_date = LazyAttribute(lambda obj: obj.start_date + timedelta(days=20))

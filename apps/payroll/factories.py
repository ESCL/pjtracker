__author__ = 'kako'

from datetime import datetime, timedelta, date

from factory import DjangoModelFactory, LazyAttribute, SubFactory

from ..accounts.factories import AccountFakeFactory
from .models import HourType, Period, CalendarDay


class CalendarDayFakeFactory(DjangoModelFactory):

    class Meta:
        model = CalendarDay

    owner = SubFactory(AccountFakeFactory)
    date = LazyAttribute(lambda obj: date.today())
    name = 'Halloween'
    type = CalendarDay.PUBLIC_HOLIDAY


class HourTypeFakeFactory(DjangoModelFactory):

    class Meta:
        model = HourType
        django_get_or_create = ('owner', 'code', )

    owner = SubFactory(AccountFakeFactory)


class NormalHoursFakeFactory(HourTypeFakeFactory):
    name = 'Standard'
    code = 'STD'


class Overtime150HoursFakeFactory(HourTypeFakeFactory):
    name = 'Overtime 150%'
    code = 'OT150'


class Overtime200HoursFakeFactory(HourTypeFakeFactory):
    name = 'Overtime 200%'
    code = 'OT200'


class PeriodFakeFactory(DjangoModelFactory):

    class Meta:
        model = Period

    owner = SubFactory(AccountFakeFactory)
    start_date = LazyAttribute(lambda obj: datetime.utcnow().date())
    end_date = LazyAttribute(lambda obj: obj.start_date + timedelta(days=30))
    forecast_start_date = LazyAttribute(lambda obj: obj.start_date + timedelta(days=20))

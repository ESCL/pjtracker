__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, SelfAttribute

from ..accounts.factories import AccountFakeFactory
from ..organizations.factories import TeamFakeFactory
from .models import TimeSheet


class TimeSheetFakeFactory(DjangoModelFactory):

    class Meta:
        model = TimeSheet

    owner = SubFactory(AccountFakeFactory)
    team = SubFactory(TeamFakeFactory, owner=SelfAttribute('..owner'))

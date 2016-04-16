__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, SelfAttribute

from ..accounts.factories import AccountFactory
from ..organizations.factories import TeamFactory
from .models import TimeSheet


class TimeSheetFactory(DjangoModelFactory):

    class Meta:
        model = TimeSheet

    owner = SubFactory(AccountFactory)
    team = SubFactory(TeamFactory, owner=SelfAttribute('..owner'))

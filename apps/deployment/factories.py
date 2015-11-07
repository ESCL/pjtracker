__author__ = 'kako'

from ..accounts.factories import UserFactory
from ..organizations.factories import TeamFactory
from .models import TimeSheet

from factory import DjangoModelFactory, SubFactory


class TimeSheetFactory(DjangoModelFactory):

    class Meta:
        model = TimeSheet

    team = SubFactory(TeamFactory)

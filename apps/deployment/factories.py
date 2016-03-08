__author__ = 'kako'

from factory import DjangoModelFactory, SubFactory, LazyAttribute

from ..organizations.factories import TeamFactory
from .models import TimeSheet


class TimeSheetFactory(DjangoModelFactory):

    class Meta:
        model = TimeSheet

    owner = LazyAttribute(lambda obj: obj.owner)
    team = SubFactory(TeamFactory)

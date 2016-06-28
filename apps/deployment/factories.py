from datetime import date, timedelta

from factory import DjangoModelFactory, SubFactory, SelfAttribute, LazyAttribute

from ..accounts.factories import AccountFakeFactory
from ..organizations.factories import TeamFakeFactory
from ..work.factories import ProjectFakeFactory
from .models import TimeSheet, ResourceProjectAssignment


class TimeSheetFakeFactory(DjangoModelFactory):

    class Meta:
        model = TimeSheet

    owner = SubFactory(AccountFakeFactory)
    team = SubFactory(TeamFakeFactory, owner=SelfAttribute('..owner'))


class ResourceProjectAssignmentFakeFactory(DjangoModelFactory):

    class Meta:
        model = ResourceProjectAssignment

    owner = SubFactory(AccountFakeFactory)
    project = SubFactory(ProjectFakeFactory, owner=SelfAttribute('..owner'))
    start_date = LazyAttribute(lambda obj: date.today())
    end_date = LazyAttribute(lambda obj: obj.start_date + timedelta(days=364))

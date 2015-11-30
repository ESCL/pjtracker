__author__ = 'kako'

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


from ....deployment.models import TimeSheetSettings, TimeSheet
from ....organizations.models import Company, Team, Position
from ....resources.models import Employee, Equipment, EquipmentType
from ....work.models import Project, Activity, ActivityGroup, ActivityGroupType, LabourType
from ...models import User
from ...utils import create_permissions


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Setting up initial groups...")

        # Admin group
        name = 'Administrators'
        print("Creating {} group...".format(name))
        group = Group.objects.create(name=name)
        group.permissions.add(*create_permissions(User, ['change']))
        group.permissions.add(*create_permissions(TimeSheetSettings, ['change']))
        print("Group {} created successfully.".format(group))

        # HR grouo
        name = 'Human Resources'
        print("Creating {} group...".format(name))
        group = Group.objects.create(name=name)
        group.permissions.add(*create_permissions(Company, ['add', 'change']))
        group.permissions.add(*create_permissions(Position, ['add', 'change']))
        group.permissions.add(*create_permissions(Employee, ['add', 'change']))
        print("Group {} created successfully.".format(group))

        # Team management
        name = 'Team Management'
        print("Creating {} group...".format(name))
        group = Group.objects.create(name=name)
        group.permissions.add(*create_permissions(Team, ['add', 'change']))
        print("Group {} created successfully.".format(group))

        # PCON group
        name = 'Project Control'
        print("Creating {} group...".format(name))
        group = Group.objects.create(name=name)
        group.permissions.add(*create_permissions(Team,  ['change activities']))
        group.permissions.add(*create_permissions(Position, ['change labour types']))
        group.permissions.add(*create_permissions(Equipment, ['add', 'change']))
        group.permissions.add(*create_permissions(EquipmentType, ['add', 'change']))
        group.permissions.add(*create_permissions(Project, ['add', 'change']))
        group.permissions.add(*create_permissions(Activity, ['add', 'change']))
        group.permissions.add(*create_permissions(ActivityGroup, ['add', 'change']))
        group.permissions.add(*create_permissions(ActivityGroupType, ['add', 'change']))
        group.permissions.add(*create_permissions(LabourType, ['add', 'change']))
        print("Group {} created successfully.".format(group))

        # Timekeeping group
        name = 'Time-Keeping'
        print("Creating {} group...".format(name))
        group = Group.objects.create(name=name)
        group.permissions.add(*create_permissions(TimeSheet, ['add', 'change', 'issue']))
        print("Group {} created successfully.".format(group))

        # Supervision group
        name = 'Supervision'
        print("Creating {} group...".format(name))
        group = Group.objects.create(name='Supervision')
        group.permissions.add(*create_permissions(TimeSheet, ['review']))
        print("Group {} created successfully.".format(group))

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
        self.stdout.write("Setting up initial groups...")

        # Admin group
        name = 'Administrators'
        self.stdout.write("Creating {} group...".format(name))
        group = Group.objects.create(name=name)
        group.permissions.add(*create_permissions(User, ['change']))
        group.permissions.add(*create_permissions(TimeSheetSettings, ['change']))
        self.stdout.write("Group {} created successfully.".format(group))

        # HR grouo
        name = 'Human Resources'
        self.stdout.write("Creating {} group...".format(name))
        group = Group.objects.create(name=name)
        group.permissions.add(*create_permissions(Company, ['add', 'change']))
        group.permissions.add(*create_permissions(Position, ['add', 'change']))
        group.permissions.add(*create_permissions(Employee, ['add', 'change']))
        self.stdout.write("Group {} created successfully.".format(group))

        # Team management
        name = 'Team Management'
        self.stdout.write("Creating {} group...".format(name))
        group = Group.objects.create(name=name)
        group.permissions.add(*create_permissions(Team, ['add', 'change']))
        self.stdout.write("Group {} created successfully.".format(group))

        # PCON group
        name = 'Project Control'
        self.stdout.write("Creating {} group...".format(name))
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
        self.stdout.write("Group {} created successfully.".format(group))

        # Timekeeping group
        name = 'Time-Keeping'
        self.stdout.write("Creating {} group...".format(name))
        group = Group.objects.create(name=name)
        group.permissions.add(*create_permissions(TimeSheet, ['add', 'change', 'issue']))
        self.stdout.write("Group {} created successfully.".format(group))

        # Supervision group
        name = 'Supervision'
        self.stdout.write("Creating {} group...".format(name))
        group = Group.objects.create(name='Supervision')
        group.permissions.add(*create_permissions(TimeSheet, ['review']))
        self.stdout.write("Group {} created successfully.".format(group))

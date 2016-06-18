__author__ = 'kako'

from django.core.management.base import BaseCommand

from ....accounts.models import User, Account
from ....organizations.models import Team
from ....work.models import Project, LabourType
from ...factories import EmployeeFakeFactory, EquipmentFakeFactory


class Command(BaseCommand):

    def handle(self, *args, **options):

        account = Account.objects.last()

        self.stdout.write("Creating example resources...")
        pj = Project.objects.last()
        hr = User.objects.filter(username__icontains='hr').last()
        pcon = User.objects.filter(username__icontains='pcon').last()
        mgt = LabourType.objects.get(code__icontains='MG')
        ind = LabourType.objects.get(code__icontains='IN')
        dir = LabourType.objects.get(code__icontains='DI')
        res = []

        # Fetch teams
        eng_team, cst_team = Team.objects.all()[:2]

        # Create resources for eng team
        res.append(EmployeeFakeFactory.create(owner=account, team=eng_team, project=pj))
        res.append(EmployeeFakeFactory.create(owner=account, team=eng_team, project=pj))
        for e in eng_team.employees:
            e.position.add_labour_type(mgt, hr)

        # Create resources for cst team
        res.append(EmployeeFakeFactory.create(owner=account, team=cst_team, project=pj))
        res.append(EmployeeFakeFactory.create(owner=account, team=cst_team, project=pj))
        res.append(EquipmentFakeFactory.create(owner=account, team=cst_team, project=pj))
        for e in cst_team.employees:
            e.position.update_labour_types([dir, ind], hr)
        for e in cst_team.equipment:
            e.type.update_labour_types([dir, ind], pcon)

        # Done, print resources
        self.stdout.write("Created resources {}.".format(res))

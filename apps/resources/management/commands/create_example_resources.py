__author__ = 'kako'

from django.core.management.base import BaseCommand

from ....accounts.models import User, Account
from ....organizations.models import Team
from ....work.models import Project, LabourType
from ...factories import EmployeeFakeFactory, EquipmentFakeFactory


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('account_code', type=str, help='Code of the account to use.')

    def handle(self, *args, **options):
        self.stdout.write("Creating example resources...")

        # Get account for the given code
        account = Account.objects.get(code=options['account_code'])

        # Get labour types and users to assign them
        mgt = LabourType.objects.get(code__icontains='MG')
        ind = LabourType.objects.get(code__icontains='IN')
        dir = LabourType.objects.get(code__icontains='DI')
        hr = User.objects.filter(owner=account, groups__name='Human Resources').last()
        pc = User.objects.filter(owner=account, groups__name='Project Control').last()

        # Fetch eng and cst teams of the account
        eng_team = Team.objects.filter(owner=account, name='Engineering').first()
        cst_team = Team.objects.filter(owner=account, name='Civil Works').first()

        # Create resources for eng team
        res = [EmployeeFakeFactory.create(owner=account, team=eng_team, company=eng_team.company)]
        res.append(EmployeeFakeFactory.create(owner=account, team=eng_team, company=eng_team.company))
        for e in eng_team.employees:
            e.position.add_labour_type(mgt, hr)

        # Create resources for cst team
        res.append(EmployeeFakeFactory.create(owner=account, team=cst_team, company=cst_team.company))
        res.append(EmployeeFakeFactory.create(owner=account, team=cst_team, company=cst_team.company))
        res.append(EquipmentFakeFactory.create(owner=account, team=cst_team, company=cst_team.company))
        for e in cst_team.employees:
            e.position.update_labour_types([dir, ind], hr)
        for e in cst_team.equipment:
            e.type.update_labour_types([dir, ind], pc)

        # Done, print resources
        self.stdout.write("Created resources {}.".format(res))

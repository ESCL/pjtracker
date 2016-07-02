__author__ = 'kako'

from django.core.management.base import BaseCommand

from ....accounts.models import Account, User
from ....work.models import Activity
from ...factories import CompanyFakeFactory, TeamFakeFactory


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('account_code', type=str, help='Code of the account to use.')

    def handle(self, *args, **options):
        self.stdout.write('Creating company...')

        # Get account for the given code
        account = Account.objects.get(code=options['account_code'])

        # Get timekeeper and supervisor user
        timekeepers = User.objects.filter(owner=account, groups__name='Time-Keeping').distinct()
        supervisors = User.objects.filter(owner=account, groups__name='Supervision').distinct()

        # Create one company
        cpy = CompanyFakeFactory.create(owner=account)

        # Create two teams
        mgt_team = TeamFakeFactory.create(
            owner=account, name='Engineering', company=cpy,
            timekeepers=timekeepers,
            supervisors=supervisors,
            activities=Activity.objects.workable()
        )
        cst_team = TeamFakeFactory.create(
            owner=account, name='Civil Works', company=cpy,
            timekeepers=timekeepers,
            supervisors=supervisors,
            activities=Activity.objects.workable()
        )

        # Done, print result
        self.stdout.write('Created company "{}" with teams {}.'.format(cpy, [mgt_team, cst_team]))

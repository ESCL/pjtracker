__author__ = 'kako'

from django.core.management.base import BaseCommand

from ....accounts.models import Account, User
from ....work.models import Activity
from ...factories import CompanyFakeFactory, TeamFakeFactory


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Creating company...')
        account = Account.objects.last()
        timekeeper = User.objects.filter(username__icontains='timekeeper').last()
        supervisor = User.objects.filter(username__icontains='supervisor').last()

        # Create one company
        cpy = CompanyFakeFactory.create(owner=account)

        # Create two teams
        mgt_team = TeamFakeFactory.create(
            owner=account, name='Engineering', company=cpy,
            timekeepers=[timekeeper],
            supervisors=[supervisor],
            activities=Activity.objects.workable()
        )
        cst_team = TeamFakeFactory.create(
            owner=account, name='Civil Works', company=cpy,
            timekeepers=[timekeeper],
            supervisors=[supervisor],
            activities=Activity.objects.workable()
        )

        # Done, print result
        self.stdout.write('Created company "{}" with teams {}.'.format(cpy, [mgt_team, cst_team]))

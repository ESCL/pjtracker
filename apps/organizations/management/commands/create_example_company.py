__author__ = 'kako'

from django.core.management.base import BaseCommand

from ....accounts.models import Account, User
from ....work.models import Activity
from ...factories import CompanyFactory, TeamFactory


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Creating company...')
        account = Account.objects.get()
        timekeeper = User.objects.get(username__icontains='timekeeper')
        supervisor = User.objects.get(username__icontains='supervisor')

        # Create one company
        cpy = CompanyFactory.create(owner=account)

        # Create two teams
        mgt_team = TeamFactory.create(name='Engineering', company=cpy,
                                      timekeepers=[timekeeper],
                                      supervisors=[supervisor],
                                      activities=Activity.objects.workable())
        cst_team = TeamFactory.create(name='Civil Works', company=cpy,
                                      timekeepers=[timekeeper],
                                      supervisors=[supervisor],
                                      activities=Activity.objects.workable())

        # Done, print result
        self.stdout.write('Created company "{}" with teams {}.'.format(cpy, [mgt_team, cst_team]))

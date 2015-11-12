__author__ = 'kako'

from django.core.management.base import BaseCommand

from ....accounts.models import Account, User
from ....work.models import Activity
from ...factories import CompanyFactory, TeamFactory


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Creating company...')
        account = Account.objects.get()
        timekeeper = User.objects.get(username='timekeeper')
        supervisor = User.objects.get(username='supervisor')
        mgt_acts = Activity.objects.filter(managerial_labour=True)
        cst_acts = Activity.objects.filter(direct_labour=True)

        # Create one company
        cpy = CompanyFactory.create(owner=account)

        # Create two teams
        mgt_team = TeamFactory.create(name='Engineering', company=cpy,
                                      timekeepers=[timekeeper],
                                      supervisors=[supervisor],
                                      activities=mgt_acts)
        cst_team = TeamFactory.create(name='Civil Works', company=cpy,
                                      timekeepers=[timekeeper],
                                      supervisors=[supervisor],
                                      activities=cst_acts)

        # Done, print result
        print('Created company "{}" with teams {}.'.format(cpy, [mgt_team, cst_team]))

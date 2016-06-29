__author__ = 'kako'

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from ...factories import UserFakeFactory, AccountFakeFactory


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Creating example account with users...")
        users = []

        # Fetch required groups
        admin = Group.objects.get(name='Administrators')
        hr = Group.objects.get(name='Human Resources')
        tmgt = Group.objects.get(name='Team Management')
        pcon = Group.objects.get(name='Project Control')
        pmgt = Group.objects.get(name='Project Management')
        tk = Group.objects.get(name='Time-Keeping')
        sup = Group.objects.get(name='Supervision')

        # Create an account
        account = AccountFakeFactory.create()

        # Create one user per group for account
        users.append(UserFakeFactory.create(username='admin', password='123', owner=account, groups=[admin]))
        users.append(UserFakeFactory.create(username='hr', password='123', owner=account, groups=[hr]))
        users.append(UserFakeFactory.create(username='tmgt', password='123', owner=account, groups=[tmgt]))
        users.append(UserFakeFactory.create(username='pcon', password='123', owner=account, groups=[pcon]))
        users.append(UserFakeFactory.create(username='pmgt', password='123', owner=account, groups=[pmgt]))
        users.append(UserFakeFactory.create(username='timekeeper', password='123', owner=account, groups=[tk]))
        users.append(UserFakeFactory.create(username='supervisor', password='123', owner=account, groups=[sup]))

        # Done, print results
        self.stdout.write('Created account "{}" with users {}.'.format(account, users))

__author__ = 'kako'

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from ...factories import UserFactory, AccountFactory


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Creating example account with users...")
        users = []

        # Fetch required groups
        admin = Group.objects.get(name='Administrators')
        hr = Group.objects.get(name='Human Resources')
        tmgt = Group.objects.get(name='Team Management')
        pcon = Group.objects.get(name='Project Control')
        tk = Group.objects.get(name='Time-Keeping')
        sup = Group.objects.get(name='Supervision')

        # Create an account
        account = AccountFactory.create()

        # Create one user per group for account
        users.append(UserFactory.create(username='admin', password='123', owner=account, groups=[admin]))
        users.append(UserFactory.create(username='hr', password='123', owner=account, groups=[hr]))
        users.append(UserFactory.create(username='tmgt', password='123', owner=account, groups=[tmgt]))
        users.append(UserFactory.create(username='pcon', password='123', owner=account, groups=[pcon]))
        users.append(UserFactory.create(username='timekeeper', password='123', owner=account, groups=[tk]))
        users.append(UserFactory.create(username='supervisor', password='123', owner=account, groups=[sup]))

        # Done, print results
        print('Created account "{}" with users {}.'.format(account, users))

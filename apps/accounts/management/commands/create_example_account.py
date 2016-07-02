__author__ = 'kako'

from django.contrib.auth.models import Group
from django.core.management import call_command, BaseCommand

from ...factories import UserFakeFactory, AccountFakeFactory


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--name', '-n', dest='name', action='store',
                            help='Name of the account to create.')
        parser.add_argument('--code', '-c', dest='code', action='store',
                            help='Code of the account to create.')
        parser.add_argument('--data', '-d', dest='data', action='store_true',
                            help='Include example data (project with resources).')

    def handle(self, *args, **options):
        self.stdout.write("Creating example account with users...")
        users = []

        # Fetch required groups
        admin = Group.objects.get(name='Administrators')
        hr = Group.objects.get(name='Human Resources')
        tm = Group.objects.get(name='Team Management')
        pc = Group.objects.get(name='Project Control')
        pm = Group.objects.get(name='Project Management')
        tk = Group.objects.get(name='Time-Keeping')
        su = Group.objects.get(name='Supervision')

        # Create an account
        data = {f: options[f] for f in ('name', 'code',) if options.get(f)}
        account = AccountFakeFactory.create(**data)

        # Create one user per group for account
        users.append(UserFakeFactory.create(username='admin', password='123', owner=account, groups=[admin]))
        users.append(UserFakeFactory.create(username='hr', password='123', owner=account, groups=[hr]))
        users.append(UserFakeFactory.create(username='tm', password='123', owner=account, groups=[tm]))
        users.append(UserFakeFactory.create(username='pc', password='123', owner=account, groups=[pc]))
        users.append(UserFakeFactory.create(username='pm', password='123', owner=account, groups=[pm]))
        users.append(UserFakeFactory.create(username='tk', password='123', owner=account, groups=[tk]))
        users.append(UserFakeFactory.create(username='su', password='123', owner=account, groups=[su]))

        # Done, print results
        self.stdout.write('Created account "{}" with users {}.'.format(account, users))

        # Add data if required
        if options['data']:
            call_command('create_example_data', account.code)

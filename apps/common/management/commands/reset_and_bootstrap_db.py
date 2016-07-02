__author__ = 'kako'

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--account-name', '-an', dest='account_name', action='store',
                            help='Name of the account to create.')
        parser.add_argument('--account-code', '-ac', dest='account_code', action='store',
                            help='Code of the account to create.')
        parser.add_argument('--data', '-d', dest='data', action='store_true',
                            help='Include example data (project with resources).')

    def handle(self, *args, **options):
        # Start by resetting the database
        call_command('reset_db')

        # Build list of params to pass to sub-command
        params = []
        if options['account_name']:
            # We have account name, add it
            params.append('-n {}'.format(options['account_name']))

            # Add code also if provided
            if options['account_code']:
                params.append('-c {}'.format(options['account_code']))

        if options['data']:
            params.append('-d')

        # Call sub-command with built params
        call_command('create_example_account', *params)

__author__ = 'kako'

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('account_code', type=str, help='Code of the account to use')

    def handle(self, *args, **options):
        # Create example data
        call_command('create_example_project', options['account_code'])
        call_command('create_example_company', options['account_code'])
        call_command('create_example_resources', options['account_code'])

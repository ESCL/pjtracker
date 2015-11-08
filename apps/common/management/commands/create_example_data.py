__author__ = 'kako'

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Create example data
        call_command('create_example_account')
        call_command('create_example_company')
        call_command('create_example_resources')
        call_command('create_example_project')
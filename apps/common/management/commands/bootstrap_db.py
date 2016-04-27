__author__ = 'kako'

from django.core.management.base import BaseCommand
from django.core.management import call_command

from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Create example account if required
        if settings.BOOTSTRAP_EXAMPLE_ACCOUNT:
            call_command('create_example_account')

        # Create example data if required
        if settings.BOOTSTRAP_EXAMPLE_DATA:
            call_command('create_example_positions')
            call_command('create_example_equipment_types')
            call_command('create_example_data')

        self.stdout.write("Done.")

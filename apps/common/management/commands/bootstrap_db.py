__author__ = 'kako'

from django.core.management.base import BaseCommand
from django.core.management import call_command

from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Create superuser
        self.stdout.write("Creating superuser...")
        call_command('createsuperuser')

        # Set up default global objects
        call_command('create_default_labour_types')
        call_command('create_default_activity_groups')

        # Create example account if required
        if settings.BOOTSTRAP_EXAMPLE_ACCOUNT:
            call_command('create_example_account')

        # Create example data if required
        if settings.BOOTSTRAP_EXAMPLE_DATA:
            call_command('create_example_positions')
            call_command('create_example_equipment_types')
            call_command('create_example_data')

        self.stdout.write("Done.")


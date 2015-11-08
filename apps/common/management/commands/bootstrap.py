__author__ = 'kako'

import os

from django.core.management.base import BaseCommand
from django.core.management import call_command

from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        db = settings.DATABASES['default']

        if 'sqlite' in db['ENGINE'].split('.')[-1]:
            # Remove sqlite database file
            print("Clearing database schema for {}...".format(db['NAME']))
            os.remove(db['NAME'])
            call_command('migrate')
        else:
            raise TypeError("You shouldn't be doing this on a real database...")

        # Create superuser
        call_command('createsuperuser')

        # Set up default global objects
        call_command('create_default_groups')
        call_command('create_default_positions')
        call_command('create_default_equipment_types')
        call_command('create_default_activity_groups')

        if settings.BOOTSTRAP_EXAMPLE:
            # Create example data for development environment
            call_command('create_example_account')
            call_command('create_example_company')
            call_command('create_example_resources')
            call_command('create_example_project')

        print("Done.")
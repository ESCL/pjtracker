__author__ = 'kako'

import os

from django.core.management.base import BaseCommand
from django.core.management import call_command

from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        db = settings.DATABASES['default']

        if 'sqlite' in db['ENGINE'].split('.')[-1]:
            # Ensure path to database parent folder exists
            parent_dir = os.path.dirname(db['NAME'])
            if not os.path.isdir(parent_dir):
                os.makedirs(parent_dir)

            # Remove sqlite database file if it exists
            if os.path.isfile(db['NAME']):
                self.stdout.write("Clearing database schema for {}...".format(db['NAME']))
                os.remove(db['NAME'])

            # Finally, call migrate
            call_command('migrate')

        else:
            raise TypeError("You shouldn't be doing this on a real database...")

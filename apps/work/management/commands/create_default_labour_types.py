__author__ = 'kako'

from django.core.management.base import BaseCommand

from ....work.factories import DirectLabourFactory, IndirectLabourFactory


class Command(BaseCommand):
    """
    Create the standard activity groups for phases and disciplines for
    construction projects.
    """
    def handle(self, **options):
        # Setup generic activity groups
        print('Setting up labour types...')

        # Create standard labour types
        types = [IndirectLabourFactory.create(),
                 DirectLabourFactory.create()]

        print('Created labour types: {}'.format(types))

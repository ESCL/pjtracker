__author__ = 'kako'

from django.core.management.base import BaseCommand

from ....work.factories import DirectLabourFactory, IndirectLabourFactory, ManagementLabourFactory


class Command(BaseCommand):
    """
    Create the standard activity groups for phases and disciplines for
    construction projects.
    """
    def handle(self, **options):
        # Setup generic activity groups
        self.stdout.write('Setting up labour types...')

        # Create standard labour types
        types = [ManagementLabourFactory.create(),
                 IndirectLabourFactory.create(),
                 DirectLabourFactory.create()]

        self.stdout.write('Created labour types: {}'.format(types))

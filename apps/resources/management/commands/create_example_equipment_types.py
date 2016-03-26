__author__ = 'kako'

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Example equipment types not defined yet, skipping...")

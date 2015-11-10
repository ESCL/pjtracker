__author__ = 'kako'

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Default equipment types not defined yet, skipping...")
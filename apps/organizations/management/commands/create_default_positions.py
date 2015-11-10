__author__ = 'kako'

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Default positions not defined yet, skipping...")
__author__ = 'kako'

from django.core.management.base import BaseCommand
from django.contrib.auth.management.commands import createsuperuser

from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        createsuperuser.Command().handle(*args, interactive=True, **options)


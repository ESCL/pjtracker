__author__ = 'kako'

import csv

from django.core.management.base import BaseCommand

from ....accounts.factories import UserBaseFactory
from ....accounts.models import Account
from ....resources.factories import EmployeeBaseFactory, EquipmentBaseFactory
from ....work.factories import ActivityBaseFactory


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('model', type=str)
        parser.add_argument('file', type=str)
        parser.add_argument('account', type=str)

    @staticmethod
    def get_factory_for(model_name):
        """
        Get the factory class matching the given model name.

        :param model_name: str
        :return: matching factory class
        """
        for f in (UserBaseFactory, EmployeeBaseFactory,
                  EquipmentBaseFactory, ActivityBaseFactory):
            if f.Meta.model.__class__.__name__.lower() == model_name.lower():
                return f
        raise ValueError("No factory found for resource '{}'.".format(model_name))

    @staticmethod
    def get_owner(account_code):
        """
        Get the owner account instance for the given account code.

        :param account_code: str
        :return: matching Account instance
        """
        return Account.objects.get(code=account_code)

    def handle(self, *args, **options):
        # Import and error file names
        if_name = options['file']
        ef_name = if_name.replace('csv', 'errors.csv')
        errors = 0

        # Select factory to use
        factory_cls = self.get_factory_for(options['model'])

        # Get owner account for all objects
        owner = self.get_owner(options['account'])

        # Open files and start cycle
        with open(options['file'], 'r') as i_file, open(ef_name, 'w') as e_file:
            # Log what we're doing
            self.stdout.write("Importing contents of '{}' as {} for {}..."
                              "".format(i_file.name, factory_cls.Meta.model, owner))

            # Open reader (for input) and writer (for errors)
            reader = csv.DictReader(i_file)
            writer = csv.DictWriter(e_file, reader.fieldnames)

            # For every row (a dict), create using factory
            for row in reader:
                try:
                    factory_cls.create(owner=owner, **row)
                except:
                    writer.writerow(row)
                    errors += 1

        # Check if we had errors, alert if so
        if errors:
            self.stdout.write("The process found {} errors, please review them"
                              " in {} and retry.".format(errors, ef_name))
        # Done
        self.stdout.write("Done.")

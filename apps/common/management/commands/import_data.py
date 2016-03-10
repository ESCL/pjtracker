__author__ = 'kako'

import re
from csv import DictReader, DictWriter

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import transaction

from ....accounts.factories import UserBaseFactory
from ....accounts.models import Account
from ....resources.factories import EmployeeBaseFactory, EquipmentBaseFactory
from ....work.factories import ActivityBaseFactory


class Command(BaseCommand):
    ERROR_SUB_RE = re.compile('^\w+ ')

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
            if f._get_model_class().__name__.lower() == model_name.lower():
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
                              "".format(i_file.name, factory_cls._get_model_class(), owner))

            # Open reader (for input) and writer (for errors)
            reader = DictReader(i_file)
            error_headers = reader.fieldnames + ['error']
            writer = DictWriter(e_file, error_headers)

            # For every row (a dict), create using factory
            for row in reader:
                e_msg = None
                try:
                    # Extract all non-empty data
                    # Note: we do this to avoid creating "empty-string instances"
                    data = {k: v for k, v in row.items() if v and k != 'error'}
                    with transaction.atomic():
                        obj = factory_cls.create(owner=owner, **data)
                        obj.full_clean()

                except KeyError as e:
                    # Error on creation, we need that field
                    e_msg = ', '.join('{} field cannot be blank'.format(a) for a in e.args)

                except ValidationError as e:
                    # Validation error, we got a dict of field: [error1, ...]
                    e_msg = ', '.join('{} {}'.format(k, self.ERROR_SUB_RE.sub('', v[0]))
                                      for k, v in e).replace('.', '')

                except Exception as e:
                    # Other error, just print
                    e_msg = str(e)

                if e_msg:
                    row['error'] = e_msg
                    writer.writerow(row)
                    errors += 1

        # Check if we had errors, alert if so
        if errors:
            self.stdout.write("The process found {} errors, please review them"
                              " in {} and retry.".format(errors, ef_name))
        # Done
        self.stdout.write("Done.")

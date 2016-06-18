__author__ = 'kako'

import re
from csv import DictReader, DictWriter
from factory import FactoryError

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError

from ....accounts.factories import UserFactory
from ....accounts.models import Account
from ....resources.factories import EmployeeFactory, EquipmentFactory
from ....work.factories import ActivityFactory


class Command(BaseCommand):
    ERROR_SUB_RE = re.compile(r'^\w+ ')
    FACTORY_ERROR_FIELD_RE = re.compile(r'\'([_\w]+)\'')

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
        for f in (UserFactory, EmployeeFactory,
                  EquipmentFactory, ActivityFactory):
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

    @classmethod
    def import_row(cls, factory, row, owner):
        """
        Create an object using the given factory, row data and owner.

        :param factory: factory of the model to create
        :param row: row data dictionary
        :param owner: Account instance that owns the object
        :return: error message
        """
        e_msg = None
        try:
            # Extract all non-empty data
            # Note: we do this to avoid creating "empty-string instances"
            data = {k: v for k, v in row.items() if v and k != 'error'}

            # Create in a transaction
            # Note: this is because all created models run a full_clean, so
            # subfactories might raise an error after the object is created,
            # in which case we want to roll back
            with transaction.atomic():
                o = factory.create(owner=owner, **data)

        except FactoryError as e:
            # Missing field (same as before, triggered by factory)
            field_name = cls.FACTORY_ERROR_FIELD_RE.search(e.args[0]).groups()[0]
            e_msg = '{} field cannot be blank'.format(field_name)

        except IntegrityError as e:
            # Error in creation, get field name from model.field
            e_msg = '{} field cannot be blank'.format(str(e).split('.')[-1])

        except ValidationError as e:
            # Validation error, we got a dict of field: [error1, ...]
            e_msg = ', '.join('{} {}'.format(k, cls.ERROR_SUB_RE.sub('', v[0]))
                              for k, v in e)

        except Exception as e:
            # Other error, just render it
            e_msg = str(e)

        return e_msg

    def handle(self, *args, **options):
        # Import and error file names
        if_name = options['file']
        ef_name = if_name.replace('csv', 'errors.csv')
        errors = 0

        # Select factory to use
        factory = self.get_factory_for(options['model'])

        # Get owner account for all objects
        owner = self.get_owner(options['account'])

        # Open files and start cycle
        with open(options['file'], 'r') as i_file, open(ef_name, 'w') as e_file:
            # Log what we're doing
            self.stdout.write("Importing contents of '{}' as {} for {}..."
                              "".format(i_file.name, factory._get_model_class(), owner))

            # Open reader (for input) and writer (for errors)
            reader = DictReader(i_file)
            error_headers = reader.fieldnames + ['error']
            writer = DictWriter(e_file, error_headers)
            writer.writeheader()

            # Now import every row
            for row in reader:
                error = self.import_row(factory, row, owner)

                # Write error if there was one (remove dots)
                if error:
                    row['error'] = error.replace('.', '')
                    writer.writerow(row)
                    errors += 1

        # Check if we had errors, alert if so
        if errors:
            self.stdout.write("The process found {} errors, please review them"
                              " in {} and retry.".format(errors, ef_name))

        # Done
        self.stdout.write("Done.")

__author__ = 'kako'

import csv
import os

from django.core.management.base import BaseCommand

from ...factories import PositionFakeFactory


class Command(BaseCommand):

    FILE_NAME = 'positions.csv'

    def handle(self, *args, **options):
        self.stdout.write('Creating example positions...')

        # Determine file path
        file_path = os.path.join(os.path.dirname(__file__), 'fixtures', self.FILE_NAME)
        self.stdout.write('Processing file {}...'.format(file_path))
        n = 0
        e = 0

        # Iterate file and create positions
        with open(os.path.join(os.path.dirname(__file__), 'fixtures', self.FILE_NAME)) as csv_file:
            reader = csv.reader(csv_file)
            for record in reader:
                pos_name = record[1]
                try:
                    PositionFakeFactory.create(name=pos_name)
                except:
                    e += 1
                else:
                    n += 1

        # Print final results
        self.stdout.write('Created {} positions, with {} errors.'.format(n, e))

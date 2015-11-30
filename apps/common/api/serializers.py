__author__ = 'kako'

import csv
import io

from tastypie.serializers import Serializer


class JsonCsvSerializer(Serializer):
    formats = ('json', 'csv',)
    content_types = {'json': 'application/json',
                     'csv': 'text/csv'}

    def to_csv(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        raw_data = io.StringIO()

        if data['objects']:
            # Flatten first object and get the headers
            flat_data = self.flatten(data['objects'][0])
            fields = flat_data.keys()

            # Init the csv dict writer
            writer = csv.DictWriter(raw_data, fields,
                                    dialect="excel",
                                    extrasaction='ignore')

            # Write header and first row
            writer.writerow(dict(zip(fields, fields)))  # In Python 2.7: `writer.writeheader()`
            writer.writerow(flat_data)

            # Write remaining rows
            for item in data['objects'][1:]:
                flat_data = self.flatten(item)
                writer.writerow(flat_data)

        return raw_data.getvalue()

    def flatten(self, data, prefix=None):
        d = {}
        for k, v in data.items():
            # First determine key
            if prefix:
                k = '{}.{}'.format(prefix, k)

            # Now determine value
            if isinstance(v, dict):
                d.update(self.flatten(v, k))
            else:
                d[k] = v
        return d

    def from_csv(self, content):
        raw_data = io.StringIO(content)
        data = []
        # Untested, so this might not work exactly right.
        for item in csv.DictReader(raw_data):
            data.append(item)
        return data


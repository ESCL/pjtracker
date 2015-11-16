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
            fields = data['objects'][0].keys()
            writer = csv.DictWriter(raw_data, fields,
                                    dialect="excel",
                                    extrasaction='ignore')
            header = dict(zip(fields, fields))
            writer.writerow(header)  # In Python 2.7: `writer.writeheader()`
            for item in data['objects']:
                writer.writerow(item)

        return raw_data.getvalue()

    def from_csv(self, content):
        raw_data = io.StringIO(content)
        data = []
        # Untested, so this might not work exactly right.
        for item in csv.DictReader(raw_data):
            data.append(item)
        return data

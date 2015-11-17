__author__ = 'kako'

from datetime import datetime

from django.db.models import Sum
from tastypie import fields

from ...common.api.resources import OwnedResource
from ...common.api.serializers import JsonCsvSerializer
from ...work.models import Activity, LabourType
from ..models import WorkLog, TimeSheet


class SummaryWorkLogQuerySet(list):

    def __init__(self, values_data):
        self.values_data = values_data
        self.activities_ids = set()
        self.labour_types_ids = set()
        self.activities = {}
        self.labour_types = {}
        self._populate_ids()
        self._fetch_objects()
        super(SummaryWorkLogQuerySet, self).__init__(self._generate_instances())

    def _populate_ids(self):
        for d in self.values_data:
            self.activities_ids.add(d.get('activity'))
            self.labour_types_ids.add(d.get('labour_type'))

    def _fetch_objects(self):
        self.activities.update({a.id: a for a in Activity.objects.filter(id__in=list(self.activities_ids))})
        self.labour_types.update({a.id: a for a in LabourType.objects.filter(id__in=list(self.labour_types_ids))})

    def _generate_instances(self):
        for pk, d in enumerate(self.values_data, 1):
            act = self.activities.get(d.get('activity'))
            lt = self.labour_types.get(d.get('labour_type'))
            yield SummaryWorklog(pk, act, lt, d['total_hours'])


class SummaryWorklog(object):

    def __init__(self, pk, activity, labour_type, total_hours):
        self.pk = pk
        self.activity = activity
        self.labour_type = labour_type
        self.total_hours = total_hours


class WorkLogResource(OwnedResource):

    class Meta:
        queryset = WorkLog.objects.all()
        fields = ('wbs_code', 'activity', 'labour', 'total_hours',)
        resource_name = 'hours'
        include_resource_uri = False
        serializer = JsonCsvSerializer(formats=('json', 'csv',))

    wbs_code = fields.CharField(attribute='activity__full_wbs_code')
    activity = fields.CharField(attribute='activity__name', null=True)
    labour = fields.CharField(attribute='labour_type__code', null=True)
    total_hours = fields.DecimalField(readonly=True, attribute='total_hours')

    def apply_filters(self, request, applicable_filters):
        qs = super(WorkLogResource, self).apply_filters(request, applicable_filters)
        values = {'activity'}

        # Add status filter if specified
        status = request.GET.get('status')
        if status == 'approved':
            qs = qs.filter(timesheet__status=TimeSheet.STATUS_APPROVED)
        elif status == 'issued':
            qs = qs.filter(timesheet__status=TimeSheet.STATUS_ISSUED)

        # Add date range filters if specified
        date_start = request.GET.get('from_date')
        date_end = request.GET.get('to_date')
        if date_start:
            qs = qs.filter(timesheet__date__gte=datetime.strptime(date_start, '%Y-%m-%d').date())
        if date_end:
            qs = qs.filter(timesheet__date__lte=datetime.strptime(date_end, '%Y-%m-%d').date())

        include = request.GET.getlist('include')
        for field in include:
            values.add(field)

        # Group by values and return
        return SummaryWorkLogQuerySet(qs.values(*values).annotate(total_hours=Sum('hours')))



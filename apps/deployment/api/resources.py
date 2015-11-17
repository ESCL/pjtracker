__author__ = 'kako'

from datetime import datetime

from django.db.models import Sum
from tastypie import fields

from ...common.api.resources import OwnedResource
from ...common.api.serializers import JsonCsvSerializer
from ..models import WorkLog, TimeSheet


class WorkLogResource(OwnedResource):

    class Meta:
        queryset = WorkLog.objects.all()
        fields = ('wbs_code', 'activity', 'labour', 'total_hours',)
        resource_name = 'hours'
        include_resource_uri = False
        serializer = JsonCsvSerializer(formats=('json', 'csv',))

    wbs_code = fields.CharField(attribute='activity__full_wbs_code')
    activity = fields.CharField(attribute='activity__name')
    labour = fields.CharField(attribute='labour_type__code')
    total_hours = fields.DecimalField(readonly=True, attribute='total_hours')

    def apply_filters(self, request, applicable_filters):
        qs = super(WorkLogResource, self).apply_filters(request, applicable_filters)

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

        return qs

    def get_object_list(self, request):
        qs = super(WorkLogResource, self).get_object_list(request)

        # Defer attributes that make it unique to group properly
        qs = qs.defer('id', 'timesheet', 'owner')
        return qs.annotate(total_hours=Sum('hours'))

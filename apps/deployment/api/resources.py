__author__ = 'kako'

from datetime import datetime

from django.db.models import Sum
from tastypie import fields, bundle

from ...common.api.resources import OwnedResource
from ...common.api.serializers import JsonCsvSerializer
from ...common.db.models import ValuesObject
from ...work.models import Activity, LabourType
from ..models import WorkLog, TimeSheet


class WorkLogResource(OwnedResource):

    class Meta:
        queryset = WorkLog.objects.all()
        fields = ('activity_code', 'activity_name', 'labour', 'hours',)
        resource_name = 'hours'
        include_resource_uri = False
        serializer = JsonCsvSerializer(formats=('json', 'csv',))
        ordering = ('activity', 'hours',)

    activity_code = fields.CharField(attribute='activity__full_wbs_code')
    activity_name = fields.CharField(attribute='activity__name', null=True)
    labour_type_code = fields.CharField(attribute='labour_type__code', null=True)
    hours = fields.DecimalField(readonly=True, attribute='total_hours')

    def apply_filters(self, request, applicable_filters):
        qs = super(WorkLogResource, self).apply_filters(request, applicable_filters)
        values = {'activity__id', 'activity__parent_id', 'activity__code', 'activity__project_id'}

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

        # Include labour type if requested
        include = request.GET.getlist('include')
        if 'labour_type' in include:
            values.update({'labour_type__id', 'labour_type__code'})

        # Group by values and return
        return qs.values(*values).annotate(total_hours=Sum('hours'))

    def build_bundle(self, obj=None, data=None, request=None, objects_saved=None):
        if obj:
            obj = ValuesObject(obj, activity=Activity, labour_type=LabourType)
        return bundle.Bundle(obj=obj, data=data, request=request,
                             objects_saved=objects_saved)


__author__ = 'kako'

from datetime import datetime

from django.db.models import Sum
from tastypie import fields, bundle

from ...common.api.resources import OwnedResource
from ...common.api.serializers import JsonCsvSerializer
from ...common.db.models import ValuesObject
from ...work.models import Activity, LabourType
from ...resources.models import Resource
from ..models import WorkLog, TimeSheet


class WorkLogResource(OwnedResource):

    class Meta:
        queryset = WorkLog.objects.all()
        fields = ('project_code', 'activity_code', 'activity_name',
                  'labour_type_code', 'labour_type_name',
                  'resource_identifier', 'hours',)
        resource_name = 'hours'
        include_resource_uri = False
        serializer = JsonCsvSerializer(formats=('json', 'csv',))
        ordering = ('activity', 'labour_type', 'resource', 'hours',)

    project_code = fields.CharField(attribute='activity__project__code', null=True)
    activity_code = fields.CharField(attribute='activity__full_wbs_code', null=True)
    activity_name = fields.CharField(attribute='activity__name', null=True)
    labour_type_code = fields.CharField(attribute='labour_type__code', null=True)
    labour_type_name = fields.CharField(attribute='labour_type__name', null=True)
    resource_identifier = fields.CharField(attribute='resource__identifier', null=True)
    resource_description = fields.CharField(attribute='resource__description', null=True)
    hours = fields.DecimalField(readonly=True, attribute='total_hours')

    def apply_filters(self, request, applicable_filters):
        qs = super(WorkLogResource, self).apply_filters(request, applicable_filters)
        values = set()

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
        group_by = request.GET.getlist('group_by')
        if not group_by or 'project' in group_by:
            values.add('activity__project_id')
        if 'activity' in group_by:
            values.update({'activity__id', 'activity__parent_id', 'activity__code', 'activity__project_id'})
        if 'labour_type' in group_by:
            values.update({'labour_type__id', 'labour_type__code', 'labour_type__name'})
        if 'resource' in group_by:
            values.update({'resource__id', 'resource__identifier', 'resource__resource_type'})

        # Group by values and return
        return qs.values(*values).annotate(total_hours=Sum('hours'))

    def build_bundle(self, obj=None, data=None, request=None, objects_saved=None):
        if obj:
            obj = ValuesObject(obj, activity=Activity, labour_type=LabourType,
                               resource=Resource)
        return bundle.Bundle(obj=obj, data=data, request=request,
                             objects_saved=objects_saved)


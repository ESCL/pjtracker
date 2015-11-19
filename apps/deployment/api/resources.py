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

    def _build_filters(self, querystring):
        filters = {}

        # Add status filter if specified
        status = querystring.get('status')
        if status == 'approved':
            filters['timesheet__status'] = TimeSheet.STATUS_APPROVED
        elif status == 'issued':
            filters['timesheet__status'] = TimeSheet.STATUS_ISSUED

        # Add date range filters if specified
        date_start = querystring.get('from_date')
        date_end = querystring.get('to_date')
        if date_start:
            filters['timesheet__date__gte'] = datetime.strptime(date_start, '%Y-%m-%d').date()
        if date_end:
            filters['timesheet__date__lte'] = datetime.strptime(date_end, '%Y-%m-%d').date()

        return filters

    def _build_groups(self, querystring):
        groups = set()
        group_by = querystring.getlist('group_by')

        # Default to grouping by project if no grouping is defined
        if not group_by or 'project' in group_by:
            groups.add('activity__project_id')

        # Check other grouping options
        if 'activity' in group_by:
            groups.update({'activity__id', 'activity__parent_id', 'activity__code',
                           'activity__name', 'activity__project_id'})
        if 'labour_type' in group_by:
            groups.update({'labour_type__id', 'labour_type__code',
                           'labour_type__name'})
        if 'resource' in group_by:
            groups.update({'resource__id', 'resource__identifier',
                           'resource__resource_type'})

        return groups

    def apply_filters(self, request, applicable_filters):
        qs = super(WorkLogResource, self).apply_filters(request, applicable_filters)

        # Get filters and grouping options
        filters = self._build_filters(request.GET)
        groups = self._build_groups(request.GET)

        # Filter, group, annotate and return
        return qs.filter(**filters).values(*groups).annotate(total_hours=Sum('hours'))


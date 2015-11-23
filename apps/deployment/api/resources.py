__author__ = 'kako'

from datetime import datetime

from django.db.models import Sum
from tastypie import fields

from ...common.api.resources import OwnedResource
from ...common.api.serializers import JsonCsvSerializer
from ..models import WorkLog, TimeSheet


class HoursResource(OwnedResource):

    class Meta:
        queryset = WorkLog.objects.all()
        fields = ('project_code', 'activity_code', 'activity_name',
                  'labour_type_code', 'labour_type_name',
                  'resource_identifier', 'date', 'hours',)
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
    date = fields.CharField(attribute='timesheet__date', null=True)
    hours = fields.DecimalField(readonly=True, attribute='total_hours')

    def apply_filters(self, request, applicable_filters):
        qs = super(HoursResource, self).apply_filters(request, applicable_filters)

        # Filter and group
        qs = qs._filter_for_querystring(request.GET)
        qs = qs._group_for_querystring(request.GET)

        # Annotate and return
        return qs.annotate(total_hours=Sum('hours'))


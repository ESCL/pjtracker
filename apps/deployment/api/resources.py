__author__ = 'kako'

from django.db.models import Sum
from tastypie import fields

from ...common.api.resources import OwnedResource
from ...common.api.serializers import JsonCsvSerializer
from ...resources.models import Resource
from ...work.models import Project, Activity, LabourType
from ..models import WorkLog


class HoursResource(OwnedResource):

    class Meta:
        queryset = WorkLog.objects.all()
        fields = ('project', 'activity_code', 'activity_name',
                  'labour_type_code', 'labour_type_name',
                  'resource_identifier', 'date', 'hours',)
        resource_name = 'hours'
        include_resource_uri = False
        serializer = JsonCsvSerializer(formats=('json', 'csv',))
        ordering = ('activity', 'labour_type', 'resource', 'hours',)

    project = fields.ToOneField('apps.deployment.api.resources.MinimalProjectResource',
                                attribute='activity__project', full=True, null=True)
    activity = fields.ToOneField('apps.deployment.api.resources.MinimalActivityResource',
                                 attribute='activity', full=True, null=True)
    labour_type = fields.ToOneField('apps.deployment.api.resources.MinimalLabourTypeResource',
                                    attribute='labour_type', full=True, null=True)
    resource = fields.ToOneField('apps.deployment.api.resources.MinimalResourceResource',
                                 attribute='resource', full=True, null=True)
    date = fields.DateField(attribute='timesheet__date', null=True)
    hours = fields.DecimalField(readonly=True, attribute='total_hours')

    def apply_filters(self, request, applicable_filters):
        qs = super(HoursResource, self).apply_filters(request, applicable_filters)

        # Store fields to display based on grouping options
        self._fields = {'hours'}
        self._fields.update(request.GET.getlist('group_by'))

        # Filter and group
        qs = qs._filter_for_querystring(request.GET)
        qs = qs._group_for_querystring(request.GET)

        # Annotate hours and return qs
        return qs.annotate(total_hours=Sum('hours'))

    def dehydrate(self, bundle):
        # Project only wanted fields
        bundle.data = {f: bundle.data[f] for f in self._fields}
        return bundle


class MinimalProjectResource(OwnedResource):

    class Meta:
        queryset = Project.objects.all()
        fields = ('code', 'name')
        include_resource_uri = False


class MinimalActivityResource(OwnedResource):

    class Meta:
        queryset = Activity.objects.all()
        fields = ('wbs_code', 'name')
        include_resource_uri = False

    wbs_code = fields.CharField(attribute='wbs_code')


class MinimalLabourTypeResource(OwnedResource):

    class Meta:
        queryset = LabourType.objects.all()
        fields = ('code', 'name')
        include_resource_uri = False


class MinimalResourceResource(OwnedResource):

    class Meta:
        queryset = Resource.objects.all()
        fields = ('identifier', 'description')
        include_resource_uri = False

    name = fields.CharField(attribute='description')
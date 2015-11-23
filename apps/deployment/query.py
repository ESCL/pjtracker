__author__ = 'kako'

from datetime import datetime

from ..common.db.query import OwnedEntityQuerySet, ValuesGroupMixin


class WorkLogQuerySet(ValuesGroupMixin, OwnedEntityQuerySet):

    def _filter_for_querystring(self, querystring):
        """
        Apply a bunch of filters according to the passed querystring.
        """
        filters = {}
        ts_model = self.model.timesheet.field.rel.to

        # Add status filter if specified
        status = querystring.get('status')
        if status == 'approved':
            filters['timesheet__status'] = ts_model.STATUS_APPROVED
        elif status == 'issued':
            filters['timesheet__status'] = ts_model.STATUS_ISSUED

        # Add date range filters if specified
        date_start = querystring.get('from_date')
        date_end = querystring.get('to_date')
        if date_start:
            filters['timesheet__date__gte'] = datetime.strptime(date_start, '%Y-%m-%d').date()
        if date_end:
            filters['timesheet__date__lte'] = datetime.strptime(date_end, '%Y-%m-%d').date()

        # Add resource type filter if required
        res_type = querystring.get('resource_type')
        if res_type:
            filters['resource__resource_type'] = res_type

        # Apply all filters and return
        return self.filter(**filters)

    def _group_for_querystring(self, querystring):
        """
        Apply a bunch of group_bys according to the passed querystring.
        """
        groups = set()
        group_by = querystring.getlist('group_by')

        # Default to grouping by project if no grouping is defined
        if not group_by or 'project' in group_by:
            groups.update({'activity__project_id'})

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

        # Return grouped queryset (a ValuesGroupQuerySet)
        return self.values(*groups)

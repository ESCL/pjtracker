__author__ = 'kako'

from django.db.models import Count
from ..common.db.query import OwnedEntityQuerySet


class ActivityQuerySet(OwnedEntityQuerySet):

    def get_or_create(self, defaults=None, **kwargs):
        """
        Process params with wbs_code before running query.
        """
        wbs_code = defaults.pop('full_wbs_code', None)
        if wbs_code:
            self.model.process_wbs_code_kwargs(wbs_code, kwargs)
        return super(ActivityQuerySet, self).get_or_create(defaults=defaults, **kwargs)

    def get_by_wbs_path(self, wbs_path):
        """
        Get an Activity matching the given WBS path, which must include the
        project code.

        Note: This will join the activity table with itself as many times
        are the are levels, to retrieve the parent in a single query.

        :param wbs_path: complete WBS path
        :return: Activity that matches the full WBS path
        """
        # Init filters with project code
        filters = {'project__code': wbs_path[0]}

        # Get parents path (-project -last)
        if wbs_path[1:]:
            # Add parents filter, as <parent__ x levels>code
            for i, code in enumerate(reversed(wbs_path[1:])):
                field = '__'.join(i * ['parent'] + ['code'])
                filters[field] = code

            # Get instance and return it (ok to fail)
            return self.get(**filters)

        else:
            # First-level activity
            return None

    def workable(self):
        """
        Filter the activities that can charge hours on any labour type.
        """
        return self.annotate(Count('labour_types')).filter(labour_types__count__gt=0)

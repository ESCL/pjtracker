__author__ = 'kako'

from django.conf.urls import url, include
from tastypie.api import Api

from .views import (ProjectView, ActivityView, ActivityGroupView,
                    ActivityGroupTypeView, LabourTypeView, ProjectWBSView)
from .api.resources import ActivityResource, ProjectResource


project_view = ProjectView.as_view()
activity_view = ActivityView.as_view()
activity_group_view = ActivityGroupView.as_view(collection_view_name='activity-groups')
activity_group_type_view = ActivityGroupTypeView.as_view(collection_view_name='activity-group-types')
labour_type_view = LabourTypeView.as_view(collection_view_name='labour-types')
project_wbs_view = ProjectWBSView.as_view()

api_v0 = Api(api_name='v0')
api_v0.register(ActivityResource())
api_v0.register(ProjectResource())

urlpatterns = [
    # Project view
    url(r'^projects/$', project_view, name='projects'),
    url(r'^projects/(?P<action>add)/$', project_view, name='project'),
    url(r'^projects/(?P<pk>\d+)/$', project_view, name='project'),
    url(r'^projects/(?P<pk>\d+)/(?P<action>edit)/$', project_view, name='project'),

    # Activity view
    url(r'^activities/$', activity_view, name='activities'),
    url(r'^activities/(?P<action>add)/$', activity_view, name='activity'),
    url(r'^activities/(?P<pk>\d+)/$', activity_view, name='activity'),
    url(r'^activities/(?P<pk>\d+)/(?P<action>edit)/$', activity_view, name='activity'),

    # Activity group view
    url(r'^activity-groups/$', activity_group_view, name='activity-groups'),
    url(r'^activity-groups/(?P<action>add)/$', activity_group_view, name='activity-group'),
    url(r'^activity-groups/(?P<pk>\d+)/$', activity_group_view, name='activity-group'),
    url(r'^activity-groups/(?P<pk>\d+)/(?P<action>edit)/$', activity_group_view, name='activity-group'),

    # Activity group type view
    url(r'^activity-group-types/$', activity_group_type_view, name='activity-group-types'),
    url(r'^activity-group-types/(?P<action>add)/$', activity_group_type_view, name='activity-group-type'),
    url(r'^activity-group-types/(?P<pk>\d+)/$', activity_group_type_view, name='activity-group-type'),
    url(r'^activity-group-types/(?P<pk>\d+)/(?P<action>edit)/$', activity_group_type_view, name='activity-group-type'),

    # Labour type view
    url(r'^labour-types/$', labour_type_view, name='labour-types'),
    url(r'^labour-types/(?P<action>add)/$', labour_type_view, name='labour-type'),
    url(r'^labour-types/(?P<pk>\d+)/$', labour_type_view, name='labour-type'),
    url(r'^labour-types/(?P<pk>\d+)/(?P<action>edit)/$', labour_type_view, name='labour-type'),

    # Experimental wbs view
    url(r'^projects/(?P<pk>\d+)/wbs/(?P<action>edit)/$', project_wbs_view, name='wbs-edit'),

    # APIs
    url(r'^api/', include(api_v0.urls))
]

__author__ = 'kako'

from django.conf.urls import url, include
from tastypie.api import Api

from .views import (ProjectView, ActivityView, ActivityGroupView,
                    ActivityGroupTypeView, LabourTypeView, ProjectWBSView)
from .api.resources import ActivityResource, ProjectResource


api_v0 = Api(api_name='v0')
api_v0.register(ActivityResource())
api_v0.register(ProjectResource())


urlpatterns = [
    # Project view
    url(r'^projects/$', ProjectView.as_view(), name='projects'),
    url(r'^projects/(?P<action>add)/$', ProjectView.as_view(), name='project'),
    url(r'^projects/(?P<pk>\d+)/$', ProjectView.as_view(), name='project'),
    url(r'^projects/(?P<pk>\d+)/(?P<action>edit)/$', ProjectView.as_view(), name='project'),

    # Activity view
    url(r'^activities/$', ActivityView.as_view(), name='activities'),
    url(r'^activities/(?P<action>add)/$', ActivityView.as_view(), name='activity'),
    url(r'^activities/(?P<pk>\d+)/$', ActivityView.as_view(), name='activity'),
    url(r'^activities/(?P<pk>\d+)/(?P<action>edit)/$', ActivityView.as_view(), name='activity'),

    # Activity group view
    url(r'^activity-groups/$', ActivityGroupView.as_view(), name='activity-groups'),
    url(r'^activity-groups/(?P<action>add)/$', ActivityGroupView.as_view(), name='activity-group'),
    url(r'^activity-groups/(?P<pk>\d+)/$', ActivityGroupView.as_view(), name='activity-group'),
    url(r'^activity-groups/(?P<pk>\d+)/(?P<action>edit)/$', ActivityGroupView.as_view(), name='activity-group'),

    # Activity group type view
    url(r'^activity-group-types/$', ActivityGroupTypeView.as_view(), name='activity-group-types'),
    url(r'^activity-group-types/(?P<action>add)/$', ActivityGroupTypeView.as_view(), name='activity-group-type'),
    url(r'^activity-group-types/(?P<pk>\d+)/$', ActivityGroupTypeView.as_view(), name='activity-group-type'),
    url(r'^activity-group-types/(?P<pk>\d+)/(?P<action>edit)/$', ActivityGroupTypeView.as_view(), name='activity-group-type'),

    # Labour type view
    url(r'^labour-types/$', LabourTypeView.as_view(), name='labour-types'),
    url(r'^labour-types/(?P<action>add)/$', LabourTypeView.as_view(), name='labour-type'),
    url(r'^labour-types/(?P<pk>\d+)/$', LabourTypeView.as_view(), name='labour-type'),
    url(r'^labour-types/(?P<pk>\d+)/(?P<action>edit)/$', LabourTypeView.as_view(), name='labour-type'),

    # Experimental wbs view
    url(r'^projects/(?P<pk>\d+)/wbs/(?P<action>edit)/$', ProjectWBSView.as_view(), name='wbs-edit'),

    # APIs
    url(r'^api/', include(api_v0.urls))
]

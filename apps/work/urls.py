__author__ = 'kako'

from django.conf.urls import url, include
from tastypie.api import Api

from .views import ProjectView, ActivityView, ProjectWBSView
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

    # Experimental wbs view
    url(r'^projects/(?P<pk>\d+)/wbs/(?P<action>edit)/$', ProjectWBSView.as_view(), name='wbs-edit'),

    # APIs
    url(r'^api/', include(api_v0.urls))
]

__author__ = 'kako'

from django.conf.urls import url, include
from tastypie.api import Api

from .views import ProjectView, ActivityView, ProjectWBSView
from .api.resources import ActivityResource


api_v0 = Api(api_name='v0')
api_v0.register(ActivityResource())


urlpatterns = [
    # Project view
    url(r'^projects/$', ProjectView.as_view(), name='projects'),
    url(r'^projects/(?P<action>add)/$', ProjectView.as_view(), name='project'),
    url(r'^projects/(?P<pk>\d+)/$', ProjectView.as_view(), name='project'),
    url(r'^projects/(?P<pk>\d+)/(?P<action>edit)/$', ProjectView.as_view(), name='project'),

    # Activity view
    url(r'^wbs/$', ActivityView.as_view(), name='activities'),
    url(r'^wbs/(?P<action>add)/$', ActivityView.as_view(), name='activity'),
    url(r'^wbs/(?P<pk>\d+)/$', ActivityView.as_view(), name='activity'),
    url(r'^wbs/(?P<pk>\d+)/(?P<action>edit)/$', ActivityView.as_view(), name='activity'),

    # Experimental wbs view
    url(r'^projects/(?P<pk>\d+)/wbs/(?P<action>edit)/$', ProjectWBSView.as_view(), name='wbs-edit'),

    # APIs
    url(r'^api/', include(api_v0.urls))
]

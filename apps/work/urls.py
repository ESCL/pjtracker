__author__ = 'kako'

from django.conf.urls import url

from .views import ProjectView, ActivityView, ProjectWBSView


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
]

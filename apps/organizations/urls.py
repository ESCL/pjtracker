__author__ = 'kako'

from django.conf.urls import url

from .views import CompanyView, DepartmentView, PositionView, TeamView


urlpatterns = [
    # Companies view
    url(r'^companies/$', CompanyView.as_view(), name='companies'),
    url(r'^companies/(?P<action>add)/$', CompanyView.as_view(), name='company'),
    url(r'^companies/(?P<pk>\d+)/$', CompanyView.as_view(), name='company'),
    url(r'^companies/(?P<pk>\d+)/(?P<action>edit)/$', CompanyView.as_view(), name='company'),

    # Companies view
    url(r'^departments/$', DepartmentView.as_view(), name='departments'),
    url(r'^departments/(?P<action>add)/$', DepartmentView.as_view(), name='department'),
    url(r'^departments/(?P<pk>\d+)/$', DepartmentView.as_view(), name='department'),
    url(r'^departments/(?P<pk>\d+)/(?P<action>edit)/$', DepartmentView.as_view(), name='department'),

    # Positions view
    url(r'^positions/$', PositionView.as_view(), name='positions'),
    url(r'^positions/(?P<action>add)/$', PositionView.as_view(), name='position'),
    url(r'^positions/(?P<pk>\d+)/$', PositionView.as_view(), name='position'),
    url(r'^positions/(?P<pk>\d+)/(?P<action>edit)/$', PositionView.as_view(), name='position'),

    # Teams view
    url(r'^teams/$', TeamView.as_view(), name='teams'),
    url(r'^teams/(?P<action>add)/$', TeamView.as_view(), name='team'),
    url(r'^teams/(?P<pk>\d+)/$', TeamView.as_view(), name='team'),
    url(r'^teams/(?P<pk>\d+)/(?P<action>edit)/$', TeamView.as_view(), name='team'),
]

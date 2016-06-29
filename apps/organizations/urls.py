__author__ = 'kako'

from django.conf.urls import url

from .views import CompanyView, DepartmentView, PositionView, TeamView


company_view = CompanyView.as_view()
department_view = DepartmentView.as_view()
position_view = PositionView.as_view()
team_view = TeamView.as_view()

urlpatterns = [
    # Companies view
    url(r'^companies/$', company_view, name='companies'),
    url(r'^companies/(?P<action>add)/$', company_view, name='company'),
    url(r'^companies/(?P<pk>\d+)/$', company_view, name='company'),
    url(r'^companies/(?P<pk>\d+)/(?P<action>edit)/$', company_view, name='company'),

    # Companies view
    url(r'^departments/$', department_view, name='departments'),
    url(r'^departments/(?P<action>add)/$', department_view, name='department'),
    url(r'^departments/(?P<pk>\d+)/$', department_view, name='department'),
    url(r'^departments/(?P<pk>\d+)/(?P<action>edit)/$', department_view, name='department'),

    # Positions view
    url(r'^positions/$', position_view, name='positions'),
    url(r'^positions/(?P<action>add)/$', position_view, name='position'),
    url(r'^positions/(?P<pk>\d+)/$', position_view, name='position'),
    url(r'^positions/(?P<pk>\d+)/(?P<action>edit)/$', position_view, name='position'),

    # Teams view
    url(r'^teams/$', team_view, name='teams'),
    url(r'^teams/(?P<action>add)/$', team_view, name='team'),
    url(r'^teams/(?P<pk>\d+)/$', team_view, name='team'),
    url(r'^teams/(?P<pk>\d+)/(?P<action>edit)/$', team_view, name='team'),
]

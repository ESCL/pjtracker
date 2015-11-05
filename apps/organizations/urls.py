__author__ = 'kako'

from django.conf.urls import url

from .views import CompanyView, TeamView


urlpatterns = [
    # Companies view
    url(r'^companies/$', CompanyView.as_view(), name='companies'),
    url(r'^companies/(?P<action>add)/$', CompanyView.as_view(), name='company'),
    url(r'^companies/(?P<pk>\d+)/$', CompanyView.as_view(), name='company'),
    url(r'^companies/(?P<pk>\d+)/(?P<action>edit)/$', CompanyView.as_view(), name='company'),

    # Teams view
    url(r'^teams/$', TeamView.as_view(), name='teams'),
    url(r'^teams/(?P<action>add)/$', TeamView.as_view(), name='team'),
    url(r'^teams/(?P<pk>\d+)/$', TeamView.as_view(), name='team'),
    url(r'^teams/(?P<pk>\d+)/(?P<action>edit)/$', TeamView.as_view(), name='team'),
]

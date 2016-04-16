__author__ = 'kako'

from django.conf.urls import url

from .views import LocationView


urlpatterns = [
    # Location view
    url(r'^locations/$', LocationView.as_view(), name='locations'),
    url(r'^locations/(?P<action>add)/$', LocationView.as_view(), name='location'),
    url(r'^locations/(?P<pk>\d+)/$', LocationView.as_view(), name='location'),
    url(r'^locations/(?P<pk>\d+)/(?P<action>edit)/$', LocationView.as_view(), name='location'),
]

__author__ = 'kako'

from django.conf.urls import url

from .views import LocationView


location_view = LocationView.as_view()

urlpatterns = [
    # Location view
    url(r'^locations/$', location_view, name='locations'),
    url(r'^locations/(?P<action>add)/$', location_view, name='location'),
    url(r'^locations/(?P<pk>\d+)/$', location_view, name='location'),
    url(r'^locations/(?P<pk>\d+)/(?P<action>edit)/$', location_view, name='location'),
]

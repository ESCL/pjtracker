__author__ = 'kako'

from django.conf.urls import url

from .views import CalendarDayView, HourTypeView


urlpatterns = [
    # Calendar days view
    url(r'^calendar/$', CalendarDayView.as_view(), name='calendar'),
    url(r'^calendar/(?P<action>add)/$', CalendarDayView.as_view(), name='calendar-day'),
    url(r'^calendar/(?P<pk>\d+)/$', CalendarDayView.as_view(), name='calendar-day'),
    url(r'^calendar/(?P<pk>\d+)/(?P<action>edit)/$', CalendarDayView.as_view(), name='calendar-day'),

    # Hour type view
    url(r'^hour-types/$', HourTypeView.as_view(), name='hour-types'),
    url(r'^hour-types/(?P<action>add)/$', HourTypeView.as_view(), name='hour-type'),
    url(r'^hour-types/(?P<pk>\d+)/$', HourTypeView.as_view(), name='hour-type'),
    url(r'^hour-types/(?P<pk>\d+)/(?P<action>edit)/$', HourTypeView.as_view(), name='hour-type'),
]

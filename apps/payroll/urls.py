__author__ = 'kako'

from django.conf.urls import url

from .views import CalendarDayView, HourTypeView, PeriodView, WorkedHoursView


calendar_day_view = CalendarDayView.as_view(collection_view_name='calendar')
hour_type_view = HourTypeView.as_view(collection_view_name='hour-types')
period_view = PeriodView.as_view()
worked_hours_view = WorkedHoursView.as_view()

urlpatterns = [
    # Calendar days view
    url(r'^calendar/$', calendar_day_view, name='calendar'),
    url(r'^calendar/(?P<action>add)/$', calendar_day_view, name='calendar-day'),
    url(r'^calendar/(?P<pk>\d+)/$', calendar_day_view, name='calendar-day'),
    url(r'^calendar/(?P<pk>\d+)/(?P<action>edit)/$', calendar_day_view, name='calendar-day'),

    # Hour type view
    url(r'^hour-types/$', hour_type_view, name='hour-types'),
    url(r'^hour-types/(?P<action>add)/$', hour_type_view, name='hour-type'),
    url(r'^hour-types/(?P<pk>\d+)/$', hour_type_view, name='hour-type'),
    url(r'^hour-types/(?P<pk>\d+)/(?P<action>edit)/$', hour_type_view, name='hour-type'),

    # Period view
    url(r'^periods/$', period_view, name='periods'),
    url(r'^periods/(?P<action>add)/$', period_view, name='period'),
    url(r'^periods/(?P<pk>\d+)/$', period_view, name='period'),
    url(r'^periods/(?P<pk>\d+)/(?P<action>edit)/$', period_view, name='period'),

    # WorkedHours view
    url(r'^periods/(?P<period_pk>\d+)/hours/$', worked_hours_view, name='worked-hours'),
    url(r'^periods/(?P<period_pk>\d+)/hours/(?P<action>process)/$', worked_hours_view, name='worked-hours'),
]

__author__ = 'kako'

from django.conf.urls import url

from .views import TimeSheetView, WorkLogsView


urlpatterns = [
    url(r'^timesheets/$', TimeSheetView.as_view(), name='timesheets'),
    url(r'^timesheets/(?P<action>add)/$', TimeSheetView.as_view(), name='timesheet'),
    url(r'^timesheets/(?P<pk>\d+)/$', TimeSheetView.as_view(), name='timesheet'),
    url(r'^timesheets/(?P<pk>\d+)/(?P<action>edit)/$', TimeSheetView.as_view(), name='timesheet'),
    url(r'^timesheets/(?P<timesheet_pk>\d+)/logs/$', WorkLogsView.as_view(), name='worklogs'),

]

__author__ = 'kako'

from django.conf.urls import url

from .views import TimeSheetView, TimeSheetActionView


urlpatterns = [
    # Timesheet view
    url(r'^timesheets/$', TimeSheetView.as_view(), name='timesheets'),
    url(r'^timesheets/(?P<action>add)/$', TimeSheetView.as_view(), name='timesheet'),
    url(r'^timesheets/(?P<pk>\d+)/$', TimeSheetView.as_view(), name='timesheet'),
    url(r'^timesheets/(?P<pk>\d+)/(?P<action>edit)/$', TimeSheetView.as_view(), name='timesheet'),

    # Timesheet action view
    url(r'^timesheets/(?P<pk>\d+)/actions/$', TimeSheetActionView.as_view(), {'action': 'add'}, name='timesheet-action'),
]

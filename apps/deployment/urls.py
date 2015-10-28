__author__ = 'kako'

from django.conf.urls import url

from .views import TimeSheetView


urlpatterns = [
    url(r'^timesheets/$', TimeSheetView.as_view(), name='timesheets'),
    url(r'^timesheets/(?P<pk>\d+)/$', TimeSheetView.as_view(), name='timesheet')
]

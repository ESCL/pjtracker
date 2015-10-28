__author__ = 'kako'

from django.conf.urls import url

from .views import EmployeeView, EquipmentView


urlpatterns = [
    url(r'^employees/$', EmployeeView.as_view(), name='employees'),
    url(r'^employees/(?P<pk>\d+)/$', EmployeeView.as_view(), name='employee'),
    url(r'^equipment/$', EquipmentView.as_view(), name='equipments'),
    url(r'^equipment/(?P<pk>\d+)/$', EquipmentView.as_view(), name='equipment'),
]

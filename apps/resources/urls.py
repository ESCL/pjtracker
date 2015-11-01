__author__ = 'kako'

from django.conf.urls import url

from .views import EmployeeView, EquipmentView


urlpatterns = [
    # Employee view
    url(r'^employees/$', EmployeeView.as_view(), name='employees'),
    url(r'^employees/(?P<action>add)/$', EmployeeView.as_view(), name='employee'),
    url(r'^employees/(?P<pk>\d+)/$', EmployeeView.as_view(), name='employee'),
    url(r'^employees/(?P<pk>\d+)/(?P<action>edit)/$', EmployeeView.as_view(), name='employee'),

    # Equipment view
    url(r'^equipment/$', EquipmentView.as_view(), name='equipments'),
    url(r'^equipment/(?P<action>add)/$', EquipmentView.as_view(), name='equipment'),
    url(r'^equipment/(?P<pk>\d+)/$', EquipmentView.as_view(), name='equipment'),
    url(r'^equipment/(?P<pk>\d+)/(?P<action>edit)/$', EquipmentView.as_view(), name='equipment'),
]

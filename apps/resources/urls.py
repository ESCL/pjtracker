__author__ = 'kako'

from django.conf.urls import url

from .views import EmployeeView, EquipmentView


urlpatterns = [
    url(r'^equipment/', EquipmentView.as_view(), name='equipment'),
    url(r'^employees/', EmployeeView.as_view(), name='employees'),
]

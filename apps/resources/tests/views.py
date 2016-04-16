__author__ = 'kako'

from django.test import TestCase

from ...common.test import PermissionTestMixin
from ..factories import EmployeeFactory, EquipmentFactory, EquipmentTypeFactory
from ..models import Employee, Equipment, EquipmentType


class EmployeeViewTest(PermissionTestMixin, TestCase):
    model = Employee
    model_factory = EmployeeFactory
    list_view_name = 'employees'
    instance_view_name = 'employee'


class EquipmentViewTest(PermissionTestMixin, TestCase):
    model = Equipment
    model_factory = EquipmentFactory
    list_view_name = 'equipments'
    instance_view_name = 'equipment'


class EquipmentTypeViewTest(PermissionTestMixin, TestCase):
    model = EquipmentType
    model_factory = EquipmentTypeFactory
    list_view_name = 'equipment-types'
    instance_view_name = 'equipment-type'

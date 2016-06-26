__author__ = 'kako'

from django.test import TestCase

from ...common.test import PermissionTestMixin
from ..factories import (EmployeeFakeFactory, EquipmentFakeFactory,
                         EquipmentTypeFakeFactory, ResourceCategoryFakeFactory,
                         ResourceProjectAssignmentFakeFactory, )
from ..models import (Employee, Equipment, EquipmentType, ResourceCategory,
                      ResourceProjectAssignment)


class EmployeeViewTest(PermissionTestMixin, TestCase):
    model = Employee
    model_factory = EmployeeFakeFactory
    list_view_name = 'employees'
    instance_view_name = 'employee'


class EquipmentViewTest(PermissionTestMixin, TestCase):
    model = Equipment
    model_factory = EquipmentFakeFactory
    list_view_name = 'equipments'
    instance_view_name = 'equipment'


class EquipmentTypeViewTest(PermissionTestMixin, TestCase):
    model = EquipmentType
    model_factory = EquipmentTypeFakeFactory
    list_view_name = 'equipment-types'
    instance_view_name = 'equipment-type'


class ResourceCategoryViewTest(PermissionTestMixin, TestCase):
    model = ResourceCategory
    model_factory = ResourceCategoryFakeFactory
    list_view_name = 'resource-categories'
    instance_view_name = 'resource-category'

# TODO: add tests for project assignment view

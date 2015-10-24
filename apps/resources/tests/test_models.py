
from django.test import TestCase

from ..factories import EmployeeFactory, EquipmentFactory


class FactoryTests(TestCase):

    def test_complex_factories(self):
        employee = EmployeeFactory.create()
        equipment = EquipmentFactory.create()

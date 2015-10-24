from django.test import TestCase

from .factories import EmployeeFactory


class EmployeeTest(TestCase):

    def test_factory(self):
        employee1 = EmployeeFactory.create()
        employee2 = EmployeeFactory.create()
        import pdb; pdb.set_trace()

        self.assertNotEqual(employee1.full_name, employee2.full_name)


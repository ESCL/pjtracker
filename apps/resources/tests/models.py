
from django.test import TestCase

from ...accounts.factories import UserFactory
from ...work.models import LabourType
from ..models import EquipmentTypeLabourType
from ..factories import EquipmentTypeFactory


class EquipmentTypeTest(TestCase):

    def setUp(self):
        super(EquipmentTypeTest, self).setUp()

        # Create a global position and labour types
        self.et = EquipmentTypeFactory.create()
        self.dir = LabourType.objects.get(code='DI')
        self.ind = LabourType.objects.get(code='IN')

    def test_add_labour_type(self):
        # Create two users with diff. accounts
        self.user1 = UserFactory.create(password='123')
        self.user2 = UserFactory.create(password='123')

        # Add direct as global
        self.et.add_labour_type(self.dir)

        # Make sure both users see it
        self.assertEqual(self.et.get_labour_types_for(self.user1).count(), 1)
        self.assertEqual(self.et.get_labour_types_for(self.user1)[0], self.dir)
        self.assertEqual(self.et.get_labour_types_for(self.user2).count(), 1)
        self.assertEqual(self.et.get_labour_types_for(self.user2)[0], self.dir)

        # User 1 also adds indirect
        self.et.add_labour_type(self.ind, self.user1)

        # Now user1 sees two, user only sees 1
        self.assertEqual(self.et.get_labour_types_for(self.user1).count(), 2)
        self.assertEqual(self.et.get_labour_types_for(self.user1)[1], self.ind)
        self.assertEqual(self.et.get_labour_types_for(self.user2).count(), 1)

        # Try to add the same again, nothing changed
        self.et.add_labour_type(self.ind, self.user1)
        self.assertEqual(self.et.get_labour_types_for(self.user1).count(), 2)
        self.assertEqual(self.et.get_labour_types_for(self.user1)[1], self.ind)
        self.assertEqual(self.et.get_labour_types_for(self.user2).count(), 1)

    def test_update_labour_types(self):
        self.user1 = UserFactory.create(password='123')

        # Update type adding only direct, should have created one for account
        self.et.update_labour_types([self.dir], self.user1)
        self.assertEqual(EquipmentTypeLabourType.objects.count(), 1)
        etlt = EquipmentTypeLabourType.objects.get()
        self.assertEqual(etlt.owner, self.user1.owner)
        self.assertEqual(etlt.equipment_type, self.et)
        self.assertEqual(etlt.labour_type, self.dir)

        # Update with indirect only, should exchange it
        self.et.update_labour_types([self.ind], self.user1)
        self.assertEqual(EquipmentTypeLabourType.objects.count(), 1)
        etlt = EquipmentTypeLabourType.objects.get()
        self.assertEqual(etlt.owner, self.user1.owner)
        self.assertEqual(etlt.equipment_type, self.et)
        self.assertEqual(etlt.labour_type, self.ind)

        # Update with both, should add only direct
        self.et.update_labour_types([self.ind, self.dir], self.user1)
        self.assertEqual(EquipmentTypeLabourType.objects.count(), 2)
        etlt = EquipmentTypeLabourType.objects.all()[1]
        self.assertEqual(etlt.owner, self.user1.owner)
        self.assertEqual(etlt.equipment_type, self.et)
        self.assertEqual(etlt.labour_type, self.dir)

        # Update with nothing, should remove it
        self.et.update_labour_types([], self.user1)
        self.assertEqual(EquipmentTypeLabourType.objects.count(), 0)

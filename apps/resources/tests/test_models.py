
from django.test import TestCase

from ...accounts.factories import UserFactory
from ...work.factories import IndirectLabourFactory, DirectLabourFactory
from ..factories import EquipmentTypeFactory


class EquipmentTypeTest(TestCase):

    def setUp(self):
        super(EquipmentTypeTest, self).setUp()

        # Create a global position and labour types
        self.et = EquipmentTypeFactory.create()
        self.dir = DirectLabourFactory.create()
        self.ind = IndirectLabourFactory.create()

    def test_labour_types(self):
        # Create two users with diff. accounts
        self.user1 = UserFactory.create()
        self.user2 = UserFactory.create()

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

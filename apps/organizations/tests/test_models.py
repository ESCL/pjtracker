from django.test import TestCase

from ...accounts.factories import UserFactory
from ...work.factories import DirectLabourFactory, IndirectLabourFactory
from ..factories import PositionFactory


class PositionTest(TestCase):

    def setUp(self):
        super(PositionTest, self).setUp()

        # Create a global position and labour types
        self.pos = PositionFactory.create()
        self.dir = DirectLabourFactory.create()
        self.ind = IndirectLabourFactory.create()

    def test_labour_types(self):
        # Create two users with diff. accounts
        self.user1 = UserFactory.create()
        self.user2 = UserFactory.create()

        # Add direct as global
        self.pos.add_labour_type(self.dir)

        # Make sure both users see it
        self.assertEqual(self.pos.get_labour_types_for(self.user1).count(), 1)
        self.assertEqual(self.pos.get_labour_types_for(self.user1)[0], self.dir)
        self.assertEqual(self.pos.get_labour_types_for(self.user2).count(), 1)
        self.assertEqual(self.pos.get_labour_types_for(self.user2)[0], self.dir)

        # User 1 also adds indirect
        self.pos.add_labour_type(self.ind, self.user1)

        # Now user1 sees two, user only sees 1
        self.assertEqual(self.pos.get_labour_types_for(self.user1).count(), 2)
        self.assertEqual(self.pos.get_labour_types_for(self.user1)[1], self.ind)
        self.assertEqual(self.pos.get_labour_types_for(self.user2).count(), 1)

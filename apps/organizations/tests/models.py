from django.test import TestCase

from ...accounts.factories import UserFactory
from ...work.models import LabourType
from ..models import PositionLabourType
from ..factories import PositionFactory


class PositionTest(TestCase):

    def setUp(self):
        super(PositionTest, self).setUp()

        # Create a global position and labour types
        self.pos = PositionFactory.create()
        self.dir = LabourType.objects.get(code='DI')
        self.ind = LabourType.objects.get(code='IN')

    def test_add_labour_type(self):
        # Create two users with diff. accounts
        self.user1 = UserFactory.create(password='123')
        self.user2 = UserFactory.create(password='123')

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

        # Try to add the same again, nothing changed
        self.pos.add_labour_type(self.ind, self.user1)
        self.assertEqual(self.pos.get_labour_types_for(self.user1).count(), 2)
        self.assertEqual(self.pos.get_labour_types_for(self.user1)[1], self.ind)
        self.assertEqual(self.pos.get_labour_types_for(self.user2).count(), 1)

    def test_update_labour_types(self):
        self.user1 = UserFactory.create(password='123')

        # Update type adding only direct, should have created one for account
        self.pos.update_labour_types([self.dir], self.user1)
        self.assertEqual(PositionLabourType.objects.count(), 1)
        plt = PositionLabourType.objects.get()
        self.assertEqual(plt.owner, self.user1.owner)
        self.assertEqual(plt.position, self.pos)
        self.assertEqual(plt.labour_type, self.dir)

        # Update with indirect only, should exchange it
        self.pos.update_labour_types([self.ind], self.user1)
        self.assertEqual(PositionLabourType.objects.count(), 1)
        plt = PositionLabourType.objects.get()
        self.assertEqual(plt.owner, self.user1.owner)
        self.assertEqual(plt.position, self.pos)
        self.assertEqual(plt.labour_type, self.ind)

        # Update with both, should add only direct
        self.pos.update_labour_types([self.ind, self.dir], self.user1)
        self.assertEqual(PositionLabourType.objects.count(), 2)
        plt = PositionLabourType.objects.all()[1]
        self.assertEqual(plt.owner, self.user1.owner)
        self.assertEqual(plt.position, self.pos)
        self.assertEqual(plt.labour_type, self.dir)

        # Update with nothing, should remove it
        self.pos.update_labour_types([], self.user1)
        self.assertEqual(PositionLabourType.objects.count(), 0)

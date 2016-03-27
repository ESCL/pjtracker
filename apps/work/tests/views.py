__author__ = 'kako'

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ...accounts.factories import UserFactory
from ...accounts.utils import ensure_permissions
from ..factories import ProjectFactory, ActivityFactory
from ..models import Project, ActivityGroupType, ActivityGroup, Activity, LabourType


class ProjectViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.p = ProjectFactory.create(owner=self.user.owner)

    def test_get(self):
        # Anon user, cannot view list of projects
        res = self.client.get(reverse('projects'))
        self.assertEqual(res.status_code, 401)

        # Login, user can now view list of projects
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('projects'))
        self.assertEqual(res.status_code, 200)

        # And also individual project
        res = self.client.get(reverse('project', kwargs={'pk': self.p.id}))
        self.assertEqual(res.status_code, 200)

        # User cannot add project
        res = self.client.get(reverse('project', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to add, user can now add project
        self.user.user_permissions.add(*ensure_permissions(Project, ['add']))
        res = self.client.get(reverse('project', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # User cannot edit project
        res = self.client.get(reverse('project', kwargs={'pk': self.p.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to edit, user can now edit project
        self.user.user_permissions.add(*ensure_permissions(Project, ['change']))
        res = self.client.get(reverse('project', kwargs={'pk': self.p.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 200)


class ActivityViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.a = ActivityFactory.create(owner=self.user.owner)

    def test_get(self):
        # Anon user, cannot view list of activities
        res = self.client.get(reverse('activities'))
        self.assertEqual(res.status_code, 401)

        # Login, user can now view list of activities
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('activities'))
        self.assertEqual(res.status_code, 200)

        # And also individual activity
        res = self.client.get(reverse('activity', kwargs={'pk': self.a.id}))
        self.assertEqual(res.status_code, 200)

        # User cannot add activity
        res = self.client.get(reverse('activity', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to add, user can now add activity
        self.user.user_permissions.add(*ensure_permissions(Activity, ['add']))
        res = self.client.get(reverse('activity', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # User cannot edit activity
        res = self.client.get(reverse('activity', kwargs={'pk': self.a.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to edit, user can now edit activity
        self.user.user_permissions.add(*ensure_permissions(Activity, ['change']))
        res = self.client.get(reverse('activity', kwargs={'pk': self.a.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 200)


class LabourTypeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.ind = LabourType.objects.get(code='IN')

    def test_get(self):
        # Anon user, cannot view list of labour types
        res = self.client.get(reverse('labour-types'))
        self.assertEqual(res.status_code, 401)

        # Login, user can now view list of labour types
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('labour-types'))
        self.assertEqual(res.status_code, 200)

        # And also individual labour type
        res = self.client.get(reverse('labour-type', kwargs={'pk': self.ind.id}))
        self.assertEqual(res.status_code, 200)

        # User cannot add labour type
        res = self.client.get(reverse('labour-type', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to add, user can now add labour type
        self.user.user_permissions.add(*ensure_permissions(LabourType, ['add']))
        res = self.client.get(reverse('labour-type', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # User cannot edit labour type
        res = self.client.get(reverse('labour-type', kwargs={'pk': self.ind.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to edit, user can now edit labour type
        self.user.user_permissions.add(*ensure_permissions(LabourType, ['change']))
        res = self.client.get(reverse('labour-type', kwargs={'pk': self.ind.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 200)



class ActivityGroupTypeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.agt = ActivityGroupType.objects.get(name='Phase')

    def test_get(self):
        # Anon user, cannot view list of activity group types
        res = self.client.get(reverse('activity-group-types'))
        self.assertEqual(res.status_code, 401)

        # Login, user can now view list of activity group types
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('activity-group-types'))
        self.assertEqual(res.status_code, 200)

        # And also individual activity group type
        res = self.client.get(reverse('activity-group-type', kwargs={'pk': self.agt.id}))
        self.assertEqual(res.status_code, 200)

        # User cannot add activity group type
        res = self.client.get(reverse('activity-group-type', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to add, user can now add activity group type
        self.user.user_permissions.add(*ensure_permissions(ActivityGroupType, ['add']))
        res = self.client.get(reverse('activity-group-type', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # User cannot edit activity group type
        res = self.client.get(reverse('activity-group-type', kwargs={'pk': self.agt.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to edit, user can now edit activity group type
        self.user.user_permissions.add(*ensure_permissions(ActivityGroupType, ['change']))
        res = self.client.get(reverse('activity-group-type', kwargs={'pk': self.agt.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 200)


class ActivityGroupViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.ag = ActivityGroup.objects.get(code='ENG')

    def test_get(self):
        # Anon user, cannot view list of activity groups
        res = self.client.get(reverse('activity-groups'))
        self.assertEqual(res.status_code, 401)

        # Login, user can now view list of activity groups
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('activity-groups'))
        self.assertEqual(res.status_code, 200)

        # And also individual activity group
        res = self.client.get(reverse('activity-group', kwargs={'pk': self.ag.id}))
        self.assertEqual(res.status_code, 200)

        # User cannot add activity group
        res = self.client.get(reverse('activity-group', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to add, user can now add activity group
        self.user.user_permissions.add(*ensure_permissions(ActivityGroup, ['add']))
        res = self.client.get(reverse('activity-group', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # User cannot edit activity group
        res = self.client.get(reverse('activity-group', kwargs={'pk': self.ag.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to edit, user can now edit activity group
        self.user.user_permissions.add(*ensure_permissions(ActivityGroup, ['change']))
        res = self.client.get(reverse('activity-group', kwargs={'pk': self.ag.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 200)

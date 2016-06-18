__author__ = 'kako'

from django.test import TestCase, Client

from ...common.test import PermissionTestMixin
from ...accounts.factories import UserFakeFactory
from ..factories import ProjectFakeFactory, ActivityFakeFactory
from ..models import Project, ActivityGroupType, ActivityGroup, Activity, LabourType


class ProjectViewTest(PermissionTestMixin, TestCase):
    model = Project
    model_factory = ProjectFakeFactory
    list_view_name = 'projects'
    instance_view_name = 'project'


class ActivityViewTest(PermissionTestMixin, TestCase):
    model = Activity
    model_factory = ActivityFakeFactory
    list_view_name = 'activities'
    instance_view_name = 'activity'


class LabourTypeViewTest(PermissionTestMixin, TestCase):
    model = LabourType
    list_view_name = 'labour-types'
    instance_view_name = 'labour-type'

    def setUp(self):
        self.client = Client()
        self.user = UserFakeFactory.create(password='123')
        self.instance = LabourType.objects.get(code='IN')


class ActivityGroupTypeViewTest(PermissionTestMixin, TestCase):
    model = ActivityGroupType
    list_view_name = 'activity-group-types'
    instance_view_name = 'activity-group-type'

    def setUp(self):
        self.client = Client()
        self.user = UserFakeFactory.create(password='123')
        self.instance = ActivityGroupType.objects.get(name='Phase')


class ActivityGroupViewTest(PermissionTestMixin, TestCase):
    model = ActivityGroup
    list_view_name = 'activity-groups'
    instance_view_name = 'activity-group'

    def setUp(self):
        self.client = Client()
        self.user = UserFakeFactory.create(password='123')
        self.instance = ActivityGroup.objects.get(code='ENG')

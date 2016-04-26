__author__ = 'kako'

from django.test import Client
from django.core.urlresolvers import reverse

from ..accounts.factories import UserFakeFactory
from ..accounts.utils import ensure_permissions


class PermissionTestMixin(object):
    """
    Mixin that provides a standard test to check all permissions for the view.
    """
    model = None
    model_factory = None
    list_view_name = None
    instance_view_name = None
    add_perm = 'add'
    edit_perm = 'change'

    def setUp(self):
        self.client = Client()
        self.user = UserFakeFactory.create(password='123')
        self.instance = self.model_factory.create(owner=self.user.owner)

    def test_permissions(self):
        # Anon view tries to view list, not allowed
        res = self.client.get(reverse(self.list_view_name))
        self.assertEqual(res.status_code, 401)

        # Login, now it can view list
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse(self.list_view_name))
        self.assertEqual(res.status_code, 200)

        # It can also view details
        res = self.client.get(reverse(self.instance_view_name, kwargs={'pk': self.instance.id}))
        self.assertEqual(res.status_code, 200)

        # But it cannot add one
        res = self.client.get(reverse(self.instance_view_name, kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Give permission to add, now it can
        self.user.user_permissions.add(*ensure_permissions(self.model, [self.add_perm]))
        res = self.client.get(reverse(self.instance_view_name, kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # But it cannot edit
        res = self.client.get(reverse(self.instance_view_name, kwargs={'pk': self.instance.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to edit, now it can
        self.user.user_permissions.add(*ensure_permissions(self.model, [self.edit_perm]))
        res = self.client.get(reverse(self.instance_view_name, kwargs={'pk': self.instance.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 200)

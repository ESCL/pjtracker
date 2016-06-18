__author__ = 'claudio.melendrez'

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ...accounts.factories import UserFakeFactory


class PublicViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_public_view(self):
        # Homepage, OK
        res = self.client.get(reverse('public', kwargs={'page': 'home'}))
        self.assertEqual(res.status_code, 200)

        # Privacy, OK
        res = self.client.get(reverse('public', kwargs={'page': 'privacy'}))
        self.assertEqual(res.status_code, 200)

        # Terms, OK
        res = self.client.get(reverse('public', kwargs={'page': 'terms'}))
        self.assertEqual(res.status_code, 200)

        # About, does not exist
        res = self.client.get(reverse('public', kwargs={'page': 'about'}))
        self.assertEqual(res.status_code, 404)

        # Made up, does not exist
        res = self.client.get(reverse('public', kwargs={'page': 'saramandanga'}))
        self.assertEqual(res.status_code, 404)


class HomeViewTest(TestCase):

    def setUp(self):
        # Create client and user
        self.client = Client()
        self.user = UserFakeFactory.create(username='pepitomadueno')

    def test_view(self):
        url = reverse('home')

        # Attempt to access, redirect to home
        res = self.client.get(url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse('public', kwargs={'page': 'home'}))

        # Login and access, now OK
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

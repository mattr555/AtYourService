from django.test import TestCase

from main.models import User, UserProfile


def create_test_user():
	user = User.objects.create_user('test1', 'test@mailinator.com', 'test1')
	prof = UserProfile(user=user, timezone='America/New_York').save()

class NavbarTest(TestCase):
	def setUp(self):
		create_test_user()
		
	def test_navbar_no_user(self):
		response = self.client.get('/')
		self.assertContains(response, 'Not logged in.')

	def test_navbar_user_logged_in(self):
		self.client.login(username='test1', password='test1')
		response = self.client.get('/')
		self.assertContains(response, 'Logged in as')
		self.assertContains(response, 'test1')

class UserTest(TestCase):
	def setUp(self):
		create_test_user()

	def test_user_login(self):
		self.client.login(username='test1', password='test1')
		response = self.client.get('/')
		self.assertEqual(response.context['user'].email, 'test@mailinator.com')

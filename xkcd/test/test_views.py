import datetime
from time import sleep
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.test import TestCase, LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from xkcd.forms import EmailUserCreationForm
from xkcd.models import Person, Like
# from xkcd.test_utils import run_pyflakes_for_package, run_pep8_for_package


class ViewTestCase(TestCase):
    def test_home_page(self):
        print "test home page"
        response = self.client.get(reverse('home'))
        self.assertIn('<p>hi, home.html</p>', response.content)

    def test_register_page(self):
        username = 'new-user'
        data = {
            'username': username,
            'email': 'test@test.com',
            'password1': 'test',
            'password2': 'test'
        }
        response = self.client.post(reverse('register'), data)

        # Check this user was created in the database
        self.assertTrue(Person.objects.filter(username=username).exists())
        print "test register page"
        # Check it's a redirect to the profile page
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTrue(response.get('location').endswith(reverse('profile')))

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertIn('Not member?', response.content)
        username = 'new-user'
        data = {
            'username': username,
            'email': 'test@test.com',
            'password1': 'test',
            'password2': 'test'
        }
        print "test login page"
        # response = self.client.post(reverse('login'), data)
        # # self.assertIsInstance(response, HttpResponseRedirect)
        # self.assertTrue(response.get('location').endswith(reverse('profile')))


    def test_profile_page(self):
        # Create user and log them in
        password = 'passsword'
        user = Person.objects.create_user(username='test-user', email='test@test.com', password=password)
        # user = PersonFactory()
        self.client.login(username=user.username, password=password)
        print "test profile page"
        # Make the url call and check the html and games queryset length
        response = self.client.get(reverse('profile'))
        self.assertIn('the last time you were here was', response.content)

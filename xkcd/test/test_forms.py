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


class FormTestCase(TestCase):
    def test_clean_username_exception(self):
        # Create a player so that this username we're testing is already taken
        Person.objects.create_user(username='test-user')

        # set up the form for testing
        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'test-user'}

        # use a context manager to watch for the validation error being raised
        with self.assertRaises(ValidationError):
            form.clean_username()

    def test_clean_username_inverse(self):

        Person.objects.create_user(username='test-user')
        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'tom'}
        self.assertEqual(form.clean_username(), "tom")
        
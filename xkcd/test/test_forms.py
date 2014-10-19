from django.core.exceptions import ValidationError
from django.test import TestCase
from xkcd.forms import EmailUserCreationForm
from xkcd.models import Person


class FormTestCase(TestCase):
    def test_clean_username_exception(self):
        Person.objects.create_user(username='test-user')
        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'test-user'}
        with self.assertRaises(ValidationError):
            form.clean_username()

    def test_clean_username_inverse(self):
        Person.objects.create_user(username='test-user')
        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'tom'}
        self.assertEqual(form.clean_username(), "tom")

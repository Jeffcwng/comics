from django.test import TestCase
from xkcd.models import Person, Like


class PersonTest(TestCase):
    def setUp(self):
        # Setup creates a Person object
        self.person = Person.objects.create(username='test')

    def test_person(self):
        # Checks to see if user was created by checking username
        self.assertEqual(self.person.username, 'test')


class LikeTest(TestCase):
    def setUp(self):
        # Setup creates a Person object and a like object with the person
        self.person = Person.objects.create(username='test-user')
        self.like = Like.objects.create(comic_name='test-name', liked_by=self.person)

    def test_like(self):
        # First checks to see if like was created
        # Then checks to see if Person was connected to Like
        self.assertEqual(self.like.comic_name, 'test-name')
        self.assertEqual(self.like.liked_by, self.person)

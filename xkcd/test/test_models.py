from django.test import TestCase
from xkcd.models import Person, Like


class PersonTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(username='test')

    def test_person(self):
        self.assertEqual(self.person.username, 'test')


class LikeTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(username='test-user')
        self.like = Like.objects.create(comic_name='test-name', url='http://test.com', liked_by=self.person)

    def test_like(self):
        self.assertEqual(self.person.username, 'test')
        self.assertEqual(self.like.comic_name, 'test-name')
        self.assertEqual(self.like.url, 'http://test.com')
        self.assertEqual(self.like.liked_by, self.person)

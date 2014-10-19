from django.test import TestCase
from xkcd.models import Person, Like


class ModelsTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(username='test-user')
        self.like = Like.objects.create(comic_name='test-name', url='http://test.com', liked_by=self.person)

    def test_person_and_like_creation(self):
        self.assertEqual(self.person.username, 'test-user')
        self.assertEqual(self.like.comic_name, 'test-name')
        self.assertEqual(self.like.url, 'http://test.com')
        self.assertEqual(self.like.liked_by, self.person)

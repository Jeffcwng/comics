from django.test import TestCase
from xkcd.models import Person, Like
from xkcd.test.factories import PersonFactory, LikesFactory


class ModelsTest(TestCase):
    def setUp(self):
        # Setup creates a Person object and a like object with the person
        self.person = Person.objects.create(username='test-user')
        self.like = Like.objects.create(
            comic_name='test-name',
            url='http://test.com',
            liked_by=self.person
        )
        self.test_person = PersonFactory()
        self.test_like = LikesFactory()

    def test_like(self):
        # First checks to see if like was created
        # Then checks to see if Person was connected to Like
        self.assertEqual(self.person.username, 'test-user')
        self.assertEqual(self.like.comic_name, 'test-name')
        self.assertEqual(self.like.url, 'http://test.com')
        self.assertEqual(self.like.liked_by, self.person)

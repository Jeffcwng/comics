from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.test import TestCase
from xkcd.models import Person, Like
from mock import patch, Mock


class ViewTestCase(TestCase):

    # Testing pre login section of site

    def test_home_page(self):
        print "test home page"
        response = self.client.get(reverse('home'))
        self.assertIn('<h1 style="text-align: center">Welcome to our amazing xkcd comic generator</h1>',
                      response.content)

    def test_register_page(self):
        username = 'new-user'
        data = {
            'username': 'new-user',
            'first_name': 'miguel',
            'last_name': 'barbosa',
            'email': 'test@test.com',
            'password1': 'test',
            'password2': 'test'
        }
        response = self.client.post(reverse('register'), data)
        self.assertTrue(Person.objects.filter(username=username).exists())
        print "test register page"
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTrue(response.get('location').endswith(reverse('comics')))

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertIn('Not member?', response.content)
        Person.objects.create_user(first_name='miguel', last_name='barbosa', username='test-user',
                                   email='test@test.com', password='password')
        data = {
            'username': 'test-user',
            'password': 'password',
        }
        print "test login page"
        response = self.client.post(reverse('login'), data)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTrue(response.get('location').endswith(reverse('comics')))

# Testing post login section of site

    def test_all_user_likes(self):
        self.user = Person.objects.create_user(first_name='miguel', last_name='barbosa', username='test-user',
                                               email='test@test.com', password='password')
        Like.objects.create(comic_name='test-name', url='http://test.com', liked_by=self.user)
        print "testing all user likes page"
        self.client.login(username='test-user', password='password')
        response = self.client.get(reverse('all_user_likes'))
        self.assertInHTML('<li>test-name<a href="http://test.com">Link to comic</a><br></li>', response.content)

    def test_comics_page(self):
        Person.objects.create_user(first_name='miguel', last_name='barbosa', username='test-user',
                                   email='test@test.com', password='password')
        print "testing comics likes page"
        self.client.login(username='test-user', password='password')
        response = self.client.get(reverse('comics'))
        self.assertInHTML('<h1>Welcome to the main area</h1>', response.content)

    def test_logout_page(self):
        Person.objects.create_user(first_name='miguel', last_name='barbosa', username='test-user',
                                   email='test@test.com', password='password')
        print "testing log out page"
        self.client.login(username='test-user', password='password')
        response = self.client.get(reverse('logout'))
        self.assertInHTML('<p>Come back soon!</p>', response.content)

    def test_profile_page(self):  # doesn't work
        Person.objects.create_user(first_name='miguel', last_name='barbosa', username='test-user',
                                   email='test@test.com', password='password')
        print "testing profile page"
        self.client.login(username='test-user', password='password')
        response = self.client.get(reverse('profile'))
        self.assertInHTML('<h2>Hi, test-user.</h2>', response.content)

    @patch('xkcd.utils.requests')  # doesn't work
    def test_random_search_page(self, mock_requests):
        mock_comic = {
            'num': 1433,
            'year': "2014",
            'safe_title': "Lightsaber",
            'alt': "A long time in the future, in a galaxy far, far, away.",
            'transcript': "An unusual gamma-ray burst originating from somewhere across the universe.",
            'img': "http://imgs.xkcd.com/comics/lightsaber.png",
            'title': "Lightsaber",
        }
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_comic
        mock_requests.get.return_value = mock_response
        Person.objects.create_user(first_name='miguel', last_name='barbosa', username='test-user',
                                   email='test@test.com', password='password')
        self.client.login(username='test-user', password='password')
        response = self.client.get(reverse('random_search'))
        self.assertIn('<h3>{} - {}</h3>'.format(mock_comic['safe_title'], mock_comic['year']),
                      response.content)
        self.assertIn('<img alt="{}" src="{}">'.format(mock_comic['alt'], mock_comic['img']),
                      response.content)

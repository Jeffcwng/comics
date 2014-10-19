from time import sleep
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.test import TestCase, LiveServerTestCase
from mock import patch, Mock
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from xkcd.forms import EmailUserCreationForm
from xkcd.models import Person, Like
from xkcd.test_utils import run_pyflakes_for_package, run_pep8_for_package

# Testing for syntax

class SyntaxTest(TestCase):
    def test_syntax(self):
        """
        Run pyflakes/pep8 across the code base to check for potential errors.
        """
        packages = ['scheduler']
        warnings = []
        for package in packages:
            warnings.extend(run_pyflakes_for_package(package, extra_ignore=("_settings",)))
            warnings.extend(run_pep8_for_package(package, extra_ignore=("_settings",)))
        if warnings:
            self.fail("{0} Syntax warnings!\n\n{1}".format(len(warnings), "\n".join(warnings)))

# Testing models


class PersonAndLikeTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(username='test-user')
        self.like = Like.objects.create(comic_name='test-name', url='http://test.com', liked_by=self.person)

    def test_person_and_like_creation(self):
        self.assertEqual(self.person.username, 'test-user')
        self.assertEqual(self.like.comic_name, 'test-name')
        self.assertEqual(self.like.url, 'http://test.com')
        self.assertEqual(self.like.liked_by, self.person)


# Testing form validation

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
        user = Person.objects.create_user(first_name='miguel', last_name='barbosa', username='test-user',
                                          email='test@test.com', password='password')
        print "testing all user likes page"
        self.client.login(username=user.username, password=user.password)
        response = self.client.get(reverse('all_user_likes'))
        print response
        self.assertInHTML('', response.content)

    def test_comics_page(self):
        user = Person.objects.create_user(first_name='miguel', last_name='barbosa', username='test-user',
                                          email='test@test.com', password='password')
        print "testing comics likes page"
        self.client.login(username=user.username, password=user.password)
        response = self.client.get(reverse('comics'))
        print response
        self.assertInHTML('', response.content)

    def test_logout_page(self):
        user = Person.objects.create_user(first_name='miguel', last_name='barbosa', username='test-user',
                                          email='test@test.com', password='password')
        print "testing log out page"
        self.client.login(username=user.username, password=user.password)
        response = self.client.get(reverse('logout'))
        self.assertInHTML('<p>Come back soon!</p>', response.content)

    def test_profile_page(self):  # doesn't work
        user = Person.objects.create_user(first_name='miguel', last_name='barbosa', username='test-user',
                                          email='test@test.com', password='password')
        print "testing profile page"
        self.client.login(username=user.username, password=user.password)
        response = self.client.get(reverse('profile'))
        print response
        self.assertInHTML('<h1>Your Profile Settings></h1>', response.content)

    @patch('cards.utils.requests')  # doesn't work
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

        response = self.client.get(reverse('home'))
        self.assertIn('<h3>{} - {}</h3>'.format(mock_comic['safe_title'], mock_comic['year']),
                      response.content)
        self.assertIn('<img alt="{}" src="{}">'.format(mock_comic['alt'], mock_comic['img']),
                      response.content)
        self.assertIn('<p>{}</p>'.format(mock_comic['transcript']), response.content)


# Selenium Tests

class SeleniumTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(SeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()

    def admin_login(self):
        Person.objects.create_superuser('superuser', 'superuser@test.com', 'mypassword')
        self.selenium.get("{}{}".format(self.live_server_url, reverse('admin:index')))
        self.selenium.find_element_by_name('username').send_keys('superuser')
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('mypassword')
        password_input.send_keys(Keys.RETURN)

    def test_admin_login(self):
        self.admin_login()
        sleep(.9)
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

    def test_admin_create_user(self):
        self.admin_login()
        sleep(.5)
        self.selenium.find_elements_by_link_text('Users')[0].click()
        sleep(.5)
        self.selenium.find_element_by_link_text('Add user').click()
        sleep(.5)
        self.selenium.find_element_by_name('password').send_keys('password')
        self.selenium.find_element_by_name('username').send_keys('TestUser')
        self.selenium.find_element_by_name('first_name').send_keys('miguel')
        self.selenium.find_element_by_name('last_name').send_keys('barbosa')
        self.selenium.find_element_by_name('email').send_keys('test@test.com')
        sleep(.5)
        self.selenium.find_element_by_css_selector("input[value='Save']").click()
        sleep(.5)
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('was added successfully', body.text)

    def test_admin_create_like(self):
        self.admin_login()
        sleep(.5)
        self.selenium.find_elements_by_link_text('Likes')[0].click()
        sleep(.5)
        self.selenium.find_element_by_link_text('Add like').click()
        sleep(.5)
        self.selenium.find_element_by_name('comic_name').send_keys('Hilarious')
        self.selenium.find_element_by_name('url').send_keys('http://www.test.com')
        self.selenium.find_element_by_name('like_status').click()
        self.selenium.find_element_by_name('liked_by').send_keys('superuser')
        sleep(2)
        self.selenium.find_element_by_css_selector("input[value='Save']").click()
        sleep(5)
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('was added successfully', body.text)

    def create_user_and_like(self):
        self.user = Person.objects.create_user(first_name='miguel', last_name='barbosa', username='test-user',
                                               email='test@test.com', password='password')
        self.like = Like.objects.create(comic_name='test-name', url='http://test.com', liked_by=self.user)
        self.like = Like.objects.create(comic_name='test-name2', url='http://test2.com', liked_by=self.user)

    def test_login_user_and_main_area(self):
        self.create_user_and_like()
        username = 'test-user'
        password = 'password'
        self.selenium.get("{}{}".format(self.live_server_url, reverse('login')))
        self.selenium.find_elements_by_link_text('Login')[0].click()
        sleep(2)
        self.selenium.find_element_by_name('username').send_keys(username)
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys(password)
        sleep(2)
        password_input.send_keys(Keys.RETURN)
        sleep(2.0)
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Welcome to the main area', body.text)

    def test_main_area_to_random_search(self):
        self.create_user_and_like()
        username = 'test-user'
        password = 'password'
        self.selenium.get("{}{}".format(self.live_server_url, reverse('login')))
        self.selenium.find_elements_by_link_text('Login')[0].click()
        sleep(1)
        self.selenium.find_element_by_name('username').send_keys(username)
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys(password)
        sleep(1)
        password_input.send_keys(Keys.RETURN)
        sleep(1.0)
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Welcome to the main area', body.text)
        sleep(1.0)
        self.selenium.find_elements_by_link_text('Find a random xkcd comic')[0].click()
        sleep(1.0)
        self.selenium.get("{}{}".format(self.live_server_url, reverse('random_search')))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn("Here's a random xkcd comic.", body.text)
        sleep(4.0)
        self.selenium.find_elements_by_id("like_this")[0].click()
        sleep(1.0)
        self.selenium.get("{}{}".format(self.live_server_url, reverse('random_search')))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn("Here's a random xkcd comic.", body.text)
        sleep(4.0)
        self.selenium.get("{}{}".format(self.live_server_url, reverse('random_search')))
        self.selenium.find_elements_by_id("find_new_cartoon")[0].click()
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn("Here's a random xkcd comic.", body.text)
        sleep(1.0)

    def test_main_area_to_likes(self):
        self.create_user_and_like()
        username = 'test-user'
        password = 'password'
        self.selenium.get("{}{}".format(self.live_server_url, reverse('login')))
        self.selenium.find_elements_by_link_text('Login')[0].click()
        sleep(2)
        self.selenium.find_element_by_name('username').send_keys(username)
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys(password)
        sleep(2)
        password_input.send_keys(Keys.RETURN)
        sleep(2.0)
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Welcome to the main area', body.text)
        sleep(1.0)
        self.selenium.find_elements_by_link_text('Browse your latest likes')[0].click()
        sleep(4.0)
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn("test-name2", body.text)
        self.assertIn("test-name", body.text)
        sleep(4.0)

    def test_profile_settings_and_password_reset(self):
        self.create_user_and_like()
        username = 'test-user'
        password = 'password'
        self.selenium.get("{}{}".format(self.live_server_url, reverse('login')))
        self.selenium.find_elements_by_link_text('Login')[0].click()
        sleep(1)
        self.selenium.find_element_by_name('username').send_keys(username)
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys(password)
        sleep(1)
        password_input.send_keys(Keys.RETURN)
        sleep(1.0)
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Welcome to the main area', body.text)
        sleep(1.0)
        self.selenium.find_elements_by_link_text('Profile/Settings')[0].click()
        sleep(1.0)
        response = self.selenium.find_element_by_tag_name('body')
        sleep(1.0)
        self.assertIn('Hi, {}.'.format(username), response.text)
        sleep(1.0)
        self.selenium.find_elements_by_link_text('Click Here')[0].click()
        sleep(1.0)
        self.selenium.find_element_by_name('email').send_keys('test@test.com')
        sleep(1.0)
        self.selenium.find_element_by_css_selector("input[value='Submit']").click()
        sleep(1.0)
        response = self.selenium.find_element_by_tag_name('body')
        sleep(1.0)
        self.assertIn('Email with password reset instructions has been sent.', response.text)
        sleep(1.0)


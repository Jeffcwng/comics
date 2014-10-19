from time import sleep
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from xkcd.models import Person, Like

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

    def test_registration_page(self):
        username = 'test-user3'
        first_name = 'miguel'
        last_name = 'barbosa'
        email = 'test3@test.com'
        password1 = 'password3'
        password2 = 'password3'
        self.selenium.get("{}{}".format(self.live_server_url, reverse('register')))
        sleep(3.0)
        self.selenium.find_element_by_name('username').send_keys(username)
        sleep(1.0)
        self.selenium.find_element_by_name('first_name').send_keys(first_name)
        sleep(1.0)
        self.selenium.find_element_by_name('last_name').send_keys(last_name)
        sleep(1.0)
        self.selenium.find_element_by_name('email').send_keys(email)
        sleep(1.0)
        self.selenium.find_element_by_name('password1').send_keys(password1)
        sleep(1.0)
        self.selenium.find_element_by_name('password2').send_keys(password2)
        sleep(1.0)
        self.selenium.find_element_by_css_selector("input[value='Submit']").click()
        sleep(2.0)
        response = self.selenium.find_element_by_tag_name('body')
        sleep(1.0)
        self.assertIn('Welcome to the main area', response.text)
        sleep(1.0)

    def create_user_and_like(self):
        self.username = 'test-user'
        self.password = 'password'
        self.user = Person.objects.create_user(
            first_name='miguel',
            last_name='barbosa',
            username=self.username,
            email='test@test.com',
            password=self.password
        )
        self.like = Like.objects.create(
            comic_name='test-name',
            url='http://test.com',
            liked_by=self.user
        )
        self.like = Like.objects.create(
            comic_name='test-name2',
            url='http://test2.com',
            liked_by=self.user
        )

    def test_login_user_and_main_area(self):
        self.create_user_and_like()
        self.selenium.get("{}{}".format(self.live_server_url, reverse('login')))
        self.selenium.find_elements_by_link_text('Login')[0].click()
        sleep(2)
        self.selenium.find_element_by_name('username').send_keys(self.username)
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys(self.password)
        sleep(2)
        password_input.send_keys(Keys.RETURN)
        sleep(2)
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Welcome to the main area', body.text)

    def test_main_area_to_random_search(self):
        self.create_user_and_like()
        like_exist = Like.objects.filter(liked_by=self.user).exists()
        self.selenium.get("{}{}".format(self.live_server_url, reverse('login')))
        self.selenium.find_elements_by_link_text('Login')[0].click()
        sleep(1)
        self.selenium.find_element_by_name('username').send_keys(self.username)
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys(self.password)
        sleep(1)
        password_input.send_keys(Keys.RETURN)
        sleep(1.0)
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Welcome to the main area', body.text)
        sleep(1.0)
        self.selenium.find_elements_by_link_text('Find a random xkcd comic')[0].click()
        sleep(1.0)
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn("Here's a random xkcd comic.", body.text)
        self.selenium.find_elements_by_id("like_this")[0].click()
        self.assertTrue(Like.objects.filter(liked_by=self.user).exists())  # fix this
        self.selenium.get("{}{}".format(self.live_server_url, reverse('random_search')))
        sleep(.5)
        self.selenium.find_elements_by_id("find_new_cartoon")[0].click()
        sleep(.5)
        body = self.selenium.find_element_by_tag_name('body')
        sleep(.5)
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

    def test_logout_page(self):
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
        self.selenium.find_elements_by_link_text('Logout')[0].click()
        sleep(3.0)
        response = self.selenium.find_element_by_tag_name('body')
        sleep(1.0)
        self.assertIn('Welcome to our amazing xkcd comic generator', response.text)
        sleep(1.0)

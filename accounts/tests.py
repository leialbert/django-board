from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
from django.urls import reverse,resolve
from .views import signup

class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code,200)
    
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func,signup)
    
    def test_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')
    
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form,UserCreationForm)
    
class SucessfulSignUpTests(TestCase):
    def setUp(self) -> None:
        url =reverse('signup')
        data = {
            'username':'john',
            'password1':'adbcdef123456',
            'password2':'adbcdef123456'
        }

        self.response = self.client.post(url,data)
        self.home_url = reverse('home')
    
    def test_redirection(self):
        self.assertRedirects(self.response,self.home_url)
    def test_user_creation(self):
        self.assertTrue(User.objects.exists())
    def test_user_authentication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidSignUpTests(TestCase):
    def setUp(self) -> None:
        url = reverse('signup')
        self.response = self.client.post(url,{})

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code,200)
    
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
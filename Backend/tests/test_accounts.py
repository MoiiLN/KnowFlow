from django.test import TestCase, Client
from django.contrib.auth.models import User

class AccountsTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username='testuser',
            password='1234'
        )

    def test_login_get(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_post_success(self):
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': '1234'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_post_fail(self):
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 200)

    def test_signup_get(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_post(self):
        response = self.client.post('/accounts/signup/', {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_logout(self):
        self.client.login(username='testuser', password='1234')
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)
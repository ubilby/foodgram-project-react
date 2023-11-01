from http import HTTPStatus

from django.test import TestCase
from rest_framework.test import APIClient

from users.models import Account


class CatsAPITestCase(TestCase):
    def setUp(self):
        data = {
            'username': 'auth_user', 'email': 'auth@us.er',
            'first_name': 'auth', 'last_name': 'user'
        }
        self.password = 'test1234'
        self.user = Account(**data)
        self.user.set_password(self.password)
        self.user.save()
        self.client = APIClient()
        self.token = self.get_token()

    def get_token(self):
        response = self.client.post(
            '/api/auth/token/login/',
            {'email': self.user.email, 'password': self.password})
        if response.status_code == 200:
            return response.data['auth_token']
        else:
            return None

    def test_authentication_exists(self):
        """Проверка работоспособности приложения через аутентификацию"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

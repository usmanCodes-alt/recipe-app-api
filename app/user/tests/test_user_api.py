from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Create and returns a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Tests for public user api"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testPass123',
            'name': 'name of the user'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user already exists with same email."""
        payload = {
            'email': 'test@example.com',
            'password': 'testPass123',
            'name': 'name of the user'
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def password_too_short_error(self):
        """Test an error is returned if password is too short"""
        payload = {
            'email': 'test@example.com',
            'password': '12',
            'name': 'name of the user'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    # def test_create_token_for_user(self):
    #     """Test create token for valid credentials"""
    #     user_details = {
    #         'name': 'Test name',
    #         'email': 'test@example.com',
    #         'password': 'test-user-password'
    #     }

    #     create_user(**user_details)

    #     payload = {
    #         'email': 'test@example.com',
    #         'password': 'test-user-password'
    #     }
    #     res = self.client.post(TOKEN_URL, payload)

    #     self.assertIn('token', res.data)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    def create_token_with_bad_credentials(self):
        """Test returns error if credentials are invalid"""
        create_user(
            email='test@example.com',
            password='goodpass'
        )

        payload = {
            'email': 'test@example.com', 'password': 'badpass'
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

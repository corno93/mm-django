
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """test the users api public"""

    def setUp(self):
        self.client = APIClient()


    def create_valid_user_success(self):
        """test valid payload works"""
        payload = {
            'email' : 'test@gmail.com',
            'password': '123456',
            'name':'testy'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get_user_model(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_when_user_exists(self):
        """test when a user already exists"""
        payload = {
            'email' : 'test@gmail.com',
            'password': '123456',
            'name':'testy'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_been_too_short(self):
        """test when a passowrd is too short"""
        payload = {
            'email' : 'test@gmail.com',
            'password': '1',
            'name':'testy'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)



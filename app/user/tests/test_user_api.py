from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")
CREATE_TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """test the users api public"""

    def setUp(self):
        self.client = APIClient()

    def create_valid_user_success(self):
        """test valid payload works"""
        payload = {"email": "test@gmail.com", "password": "123456", "name": "testy"}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get_user_model(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_when_user_exists(self):
        """test when a user already exists"""
        payload = {"email": "test@gmail.com", "password": "123456", "name": "testy"}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_been_too_short(self):
        """test when a passowrd is too short"""
        payload = {"email": "test@gmail.com", "password": "1", "name": "testy"}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        payload = {"email": "test@gmail.com", "password": "12341234"}
        create_user(**payload)
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        create_user(email="test@gmail.com", password="123123")
        payload = {"email": "test@gmail.com", "password": "somethingwrong"}
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user(
            email="test@gmail.com",
            password="password",
            name="alex",
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_user_profile(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"name": self.user.name, "email": self.user.email})

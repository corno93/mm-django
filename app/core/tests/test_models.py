from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_sucessful(self):
        """Testing creating user with email"""
        email = "test@gmail.com"
        password = "test1234"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalizing_email(self):
        """test email for a new user is normalized"""
        email = "test@GMAIL.com"
        password = "test1234"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email.lower())
        self.assertTrue(user.check_password(password))

    def test_invalid_email(self):
        """test error raised when no email is provided"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None, password="password123"
            )

    def test_create_new_super_user(self):
        """test a super user has is_staff"""
        email = "test@gmail.com"
        password = "test1234"
        user = get_user_model().objects.create_super_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email.lower())
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

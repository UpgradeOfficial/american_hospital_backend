import uuid
from typing import Dict
from unittest.mock import patch

from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from core.utils import ExpiringActivationTokenGenerator
from user.models import User

from .factories import create_test_user, user_password, create_test_password_reset_token
from .test_literals import user_registration_info

# Create your tests here.


class UserRegistrationTestCase(object):
    def setUp(self):
        """This should never execute but it does when I test test_store_a"""
        self.url = None
        self.data = user_registration_info

    def update_data(self, data: Dict):
        self.data.update(data)

    def remove_key_from_data(self, key):
        self.data.pop(key, None)

    def _test_user_registration_right_information(self):
        url = reverse(self.url)
        response = self.client.post(url, data=self.data)
        self.assertEqual(
            response.status_code, 201
        ) if response.status_code == 201 else None
        self.assertEqual(
            mail.outbox[0].subject, f"Verify User Account {self.data['email']}"
        ) if response.status_code == 201 else None
        self.assertEqual(
            mail.outbox[0].from_email, settings.EMAIL_HOST_USER
        ) if response.status_code == 201 else None
        return response


class UserModel(TestCase):
    def setUp(self):
        self.user1 = create_test_user(is_deleted=True)
        self.user2 = create_test_user(is_deleted=True)
        self.user3 = create_test_user()
        self.user4 = create_test_user()
        self.user5 = create_test_user()

    def test_user_manager_all_returns_only_undeleted_objects(self):
        users = User.objects.all()
        self.assertEqual(len(users), 3)

    def test_user_manager_soft_delete_function(self):
        User.objects.delete()
        users_after_delete = User.objects.all()
        self.assertEqual(len(users_after_delete), 0)

    def test_soft_delete__of_object(self):
        self.user3.delete()
        user = User.all_objects.get(id=self.user3.id)
        self.assertEquals(user.is_deleted, True)
        self.assertIsNotNone(user.deleted_at)


class ChangePasswordTest(TestCase):
    @patch("rest_framework_simplejwt.authentication.JWTAuthentication.authenticate")
    def test_password_change_with_authenticated_user(self, authenticate_function):
        user = create_test_user()
        authenticate_function.return_value = user, None
        url = reverse("user:change_password")
        old_password = user_password
        new_password = "new_password"
        data = {"old_password": old_password, "new_password": new_password}
        response = self.client.patch(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.first().check_password(new_password))

    def test_password_change_with_unauthenticated_user(self):
        url = reverse("user:change_password")
        old_password = user_password
        new_password = "new_password"
        data = {"old_password": old_password, "new_password": new_password}
        response = self.client.patch(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 403)

    @patch("rest_framework_simplejwt.authentication.JWTAuthentication.authenticate")
    def test_password_change_with_wrong_old_password(self, authenticate_function):
        user = create_test_user()
        authenticate_function.return_value = user, None
        url = reverse("user:change_password")
        old_password = user_password + "wrong_string"
        new_password = "new_password"
        data = {"old_password": old_password, "new_password": new_password}
        response = self.client.patch(url, data=data, content_type="application/json")
        # response_data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.first().check_password(new_password))

    @patch("rest_framework_simplejwt.authentication.JWTAuthentication.authenticate")
    def test_password_change_with_old_password_equals_new(self, authenticate_function):
        user = create_test_user()
        authenticate_function.return_value = user, None
        url = reverse("user:change_password")
        old_password = user_password
        new_password = user_password
        data = {"old_password": old_password, "new_password": new_password}
        response = self.client.patch(url, data=data, content_type="application/json")
        # response_data = response.json()
        self.assertEqual(response.status_code, 400)


class InitialPasswordResetTest(TestCase):
    def setUp(self):
        self.user = create_test_user(email="odeyemiincrease@yahoo.com")

    def test_initiate_password_reset_with_email_that_exists(self):
        url = reverse("user:initiate_password_reset")
        data = {"email": self.user.email}
        response = self.client.post(url, data)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            response_data["message"], "Email Has Been sent to the email provided"
        )
        self.assertEqual(mail.outbox[0].subject, "Password Reset")
        self.assertEqual(mail.outbox[0].from_email, settings.EMAIL_HOST_USER)
        self.assertEqual(mail.outbox[0].to, [self.user.email])

    def test_initiate_password_reset_with_email_that_dont_exists(self):
        url = reverse("user:initiate_password_reset")
        data = {"email": "unknown@gmail.com"}
        response = self.client.post(url, data)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_data["message"], "Email Has Been sent to the email provided"
        )
        self.assertEqual(len(mail.outbox), 0)


class CompletePasswordResetTest(TestCase):
    def setUp(self):
        self.user = create_test_user(email="odeyemiincrease@yahoo.com")

    def test_password_reset_with_email_that_exists_and_token(self):
        url = reverse("user:complete_password_reset")
        password_reset_object = create_test_password_reset_token(email=self.user.email)
        data = {"password": "new_password", "token": password_reset_object.token}
        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password(user_password))
        self.assertFalse((user.check_password(data["password"])))
        response = self.client.post(url, data)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password(data["password"]))
        self.assertFalse(user.check_password(user_password))
        self.assertEqual(response_data["message"], "Password Reset Completed")

    def test_password_reset_with_email_that_exists_and_invalid_token(self):
        url = reverse("user:complete_password_reset")
        password_reset_object = create_test_password_reset_token(email=self.user.email)
        data = {"password": "new_password", "token": f"{password_reset_object}-invalid"}
        response = self.client.post(url, data)
        response_data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_data["error"],
            ["Invalid Token. Password Rest Record Doesn't Exists"],
        )

    def test_password_used_token(self):
        url = reverse("user:complete_password_reset")
        password_reset_object = create_test_password_reset_token(email=self.user.email)
        data = {"password": "new_password", "token": password_reset_object.token}
        self.client.post(url, data)
        response = self.client.post(url, data)
        response_data = response.json()
        self.assertEqual(
            response_data["error"],
            ["Invalid Token. Password Rest Record Doesn't Exists"],
        )


class ConfirmUserEmail(TestCase):
    def setUp(self):
        self.user = create_test_user()
        self.token_object = ExpiringActivationTokenGenerator()

    def test_confirm_with_email_that_exists_and_token(self):
        token = str(self.token_object.generate_token(self.user.email).decode("utf-8"))
        url = reverse("user:confirm_email")
        data = {"token": token}
        response = self.client.post(url, data=data)
        response_data = response.json()
        user = User.objects.get(id=self.user.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["message"], "Email Verification successful")
        self.assertEqual(user.is_verified, True)

    def test_confirm_with_invalid_token(self):
        token = (
            self.token_object.generate_token(self.user.email).decode("utf-8")
            + "1234567890123456789012345678901"
        )
        url = reverse("user:confirm_email")
        data = {"token": token}
        response = self.client.post(url, data=data)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(user.is_verified, False)

    # ? this is for latter testing

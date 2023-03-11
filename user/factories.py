import random
from datetime import date, datetime, timedelta

import factory

from core.utils import ExpiringActivationTokenGenerator
from user.models import PasswordResetWhitelist, User

user_password = "aaaaaaaaaaa"


def create_test_user(
    user_type=User.UserType.PATIENT, is_deleted=False, is_verified=False, email=None
):
    email = email or f"a{random.randint(0, 1000000000000000)}@b.c"
    user = User.objects.create_user(
        email=email,
        password=user_password,
        user_type=user_type,
        is_verified=is_verified,
        is_deleted=is_deleted,
        date_of_birth=date.today(),
    )
    return user


def create_test_password_reset_token(email, token=None):
    token = ExpiringActivationTokenGenerator().generate_token(text=email)
    password_reset_object = PasswordResetWhitelist.objects.create(
        email=email, token=token.decode("utf-8")
    )
    return password_reset_object


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        exclude = ("now",)

    now = factory.LazyFunction(datetime.utcnow)
    date_of_birth = factory.LazyAttribute(lambda o: o.now - timedelta(weeks=1400))
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

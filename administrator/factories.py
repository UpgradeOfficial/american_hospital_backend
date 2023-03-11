import factory

from user.factories import UserFactory
from user.models import User

from .models import Administrator


class AdministratorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Administrator

    user = factory.SubFactory(UserFactory, user_type=User.UserType.ADMINISTRATOR)

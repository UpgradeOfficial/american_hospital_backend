import factory
from .models import Administrator
from user.factories import UserFactory
from user.models import User


class AdministratorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Administrator

    user = factory.SubFactory(UserFactory, user_type=User.UserType.ADMINISTRATOR)

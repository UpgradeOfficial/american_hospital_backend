import factory

from user.factories import UserFactory, create_test_user

from .models import Patient


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Patient

    user = factory.SubFactory(UserFactory)

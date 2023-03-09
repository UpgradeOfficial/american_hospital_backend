from user.factories import create_test_user, UserFactory
from .models import Patient
import factory


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Patient

    user = factory.SubFactory(UserFactory)

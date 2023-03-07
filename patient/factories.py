from user.factories import create_test_user, UserFactory
from .models import Patient
import factory


def create_test_patient(user=None):
    user = user or create_test_user()
    patient = Patient.objects.create(
        user=user,
    )
    return patient


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Patient

    user = factory.SubFactory(UserFactory)

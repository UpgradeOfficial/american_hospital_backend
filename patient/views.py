from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from administrator.permissions import AdministratorPermission
from patient.models import Patient

from .serializers import PatientProfileDetailsSerializer, PatientRegistrationSerializer


class PatientRegistrationView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = PatientRegistrationSerializer


class PatientListView(generics.ListAPIView):
    permission_classes = [AdministratorPermission]
    serializer_class = PatientProfileDetailsSerializer

    def get_queryset(self):
        return Patient.objects.all()


class PatientProfileDetailsAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = PatientProfileDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.all()

    def get_object(self):
        return Patient.objects.get(user=self.request.user)

from rest_framework import generics
from patient.models import Patient

from .serializers import PatientProfileDetailsSerializer, PatientRegistrationSerializer
from rest_framework.permissions import IsAuthenticated


class PatientRegistrationView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = PatientRegistrationSerializer


class PatientListView(generics.ListAPIView):
    permission_classes = []
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

from rest_framework import generics

from administrator.permissions import AdministratorPermission

from .models import Testimonial
from .serializers import TestimonialPublicSerializer, TestimonialSerializer


class TestimonialCreateView(generics.CreateAPIView):
    serializer_class = TestimonialSerializer
    permission_classes = [AdministratorPermission]


class TestimonialListView(generics.ListAPIView):
    serializer_class = TestimonialPublicSerializer
    permission_classes = []

    def get_queryset(self):
        return Testimonial.objects.all()


class TestimonialRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestimonialSerializer
    permission_classes = [AdministratorPermission]

    def get_queryset(self):
        return Testimonial.objects.all()

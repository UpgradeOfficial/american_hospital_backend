from django.shortcuts import render
from rest_framework import generics

from administrator.permissions import AdministratorPermission

from .models import FAQ
from .serializers import FAQSerializer

# Create your views here.


class FAQCreateView(generics.CreateAPIView):
    permission_classes = [AdministratorPermission]
    serializer_class = FAQSerializer


class FAQListView(generics.ListAPIView):
    permission_classes = []
    serializer_class = FAQSerializer

    def get_queryset(self):
        return FAQ.objects.all()


class FAQRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AdministratorPermission]
    serializer_class = FAQSerializer

    def get_queryset(self):
        return FAQ.objects.all()

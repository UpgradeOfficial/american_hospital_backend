from django.shortcuts import render

from rest_framework import generics
from patient.models import Patient

from .serializers import CategoryViewSerializer, NewsViewSerializer
from rest_framework.permissions import IsAuthenticated


class CategoryView(generics.CreateAPIView):
    permission_classes =  ['IsAdminUser']
    serializer_class = CategoryViewSerializer


class NewsView(generics.CreateAPIView):
    permission_classes = ['IsAdminUser']
    serializer_class = NewsViewSerializer

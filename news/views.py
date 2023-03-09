from django.shortcuts import render

from rest_framework import generics
from administrator.permissions import AdministratorPermission
from news.models import Category, News
from patient.models import Patient

from .serializers import CategoryListSerializer, CategoryViewSerializer, NewsListSerializer, NewsViewSerializer
from rest_framework.permissions import IsAuthenticated


class CategoryView(generics.CreateAPIView):
    permission_classes =  [AdministratorPermission]
    serializer_class = CategoryViewSerializer

class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    permission_classes = [AdministratorPermission]

    def get_queryset(self):
        return Category.objects.all()
    
class CategoryRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryViewSerializer
    permission_classes = [AdministratorPermission]

    def get_queryset(self):
        return Category.objects.all()


class NewsCreateView(generics.CreateAPIView):
    permission_classes = [AdministratorPermission]
    serializer_class = NewsViewSerializer


class NewsListView(generics.ListAPIView):
    serializer_class = NewsListSerializer
    permission_classes = [AdministratorPermission]

    def get_queryset(self):
        return News.objects.all()

class NewsRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsViewSerializer
    permission_classes = [AdministratorPermission]

    def get_queryset(self):
        return News.objects.all()
from rest_framework import generics

from administrator.permissions import AdministratorPermission
from news.models import Category, News

from .serializers import CategorySerializer, NewsSerializer


class CategoryCreateView(generics.CreateAPIView):
    permission_classes = [AdministratorPermission]
    serializer_class = CategorySerializer


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = []

    def get_queryset(self):
        return Category.objects.all()


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AdministratorPermission]

    def get_queryset(self):
        return Category.objects.all()


class NewsCreateView(generics.CreateAPIView):
    permission_classes = [AdministratorPermission]
    serializer_class = NewsSerializer


class NewsListView(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = []

    def get_queryset(self):
        return News.objects.all()


class NewsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsSerializer
    permission_classes = [AdministratorPermission]

    def get_queryset(self):
        return News.objects.all()

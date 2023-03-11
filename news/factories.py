import factory

from .models import Category, News


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category


class NewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = News

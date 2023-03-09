from rest_framework.serializers import (
    ModelSerializer,
)
from news.models import Category, News


class CategoryViewSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class NewsViewSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"
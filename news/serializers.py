from rest_framework import serializers

from news.models import Category, News


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "id"]


class NewsSerializer(serializers.ModelSerializer):
    # categories = CategorySerializer(many=True)
    class Meta:
        model = News
        fields = "__all__"

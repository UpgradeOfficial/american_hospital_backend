from rest_framework import serializers

from .models import Testimonial


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"

    def create(self, validated_data):
        creator = self.context["request"].user
        validated_data["creator"] = creator
        print(validated_data, "------------")
        return super().create(validated_data)


class TestimonialPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ["content", "name_of_author"]

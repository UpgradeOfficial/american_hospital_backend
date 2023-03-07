from rest_framework import serializers
from patient.models import Patient
from user.models import User
from user.serializers import UserRegistrationSerializer, UserProfileSerializer
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    DateField,
    EmailField,
    ChoiceField,
    FileField,
)


class PatientRegistrationSerializer(UserRegistrationSerializer):
    class Meta:
        model = User
        write_only_fields = [
            # User fields
            "first_name",
            "last_name",
            "password",
            "email",
            "street",
            "state",
            "city",
            "region",
            "country",
            "contact_no",
            "date_of_birth",
            "gender",
            "image",
            # patient fields
        ]
        fields = write_only_fields

    def create(self, validated_data):
        validated_data["user_type"] = User.UserType.PATIENT
        user = super().create(validated_data)
        Patient.objects.create(user=user)
        return user


class PatientProfileDetailsSerializer(ModelSerializer):
    first_name = CharField(source="user.first_name", required=False, allow_null=True)
    last_name = CharField(source="user.last_name", required=False, allow_null=True)
    contact_no = CharField(source="user.contact_no", required=False, allow_null=True)
    profile_photo = FileField(
        source="user.profile_photo", required=False, allow_null=True
    )
    date_of_birth = DateField(
        source="user.date_of_birth",
        required=False,
        allow_null=True,
    )
    gender = ChoiceField(
        source="user.gender", choices=User.Gender.choices, required=False
    )
    email = EmailField(source="user.email", read_only=True)
    street = CharField(source="user.street", required=False)
    city = CharField(source="user.city", required=False)
    state = CharField(source="user.state", required=False)
    zip_code = CharField(source="user.zip_code", required=False)
    country = CharField(source="user.country", required=False)
    region = CharField(source="user.region", required=False)

    class Meta:
        model = Patient
        user_fields = [
            "first_name",
            "last_name",
            "contact_no",
            "profile_photo",
            "date_of_birth",
            "gender",
            "email",
            "street",
            "region",
            "city",
            "state",
            "zip_code",
            "country",
            "region",
        ]
        fields = "__all__"
        read_only_fields = [
            "email",
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user_serializer = UserProfileSerializer(
            instance=instance.user, data=user_data, partial=True
        )
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return super().update(instance, validated_data)

from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from .tasks import send_email_verification_mail_async
from .validators import verify_valid_mail


class UserRegistrationSerializer(serializers.ModelSerializer):
    # tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ["groups", "user_permissions", "is_staff"] + User.get_hidden_fields()
        read_only_fields = ("is_active",)
        extra_kwargs = {
            "user_type": {"read_only": True},
            "password": {"write_only": True},
        }

    def validate_email(self, email):
        return verify_valid_mail(email)

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        if password is None:
            raise serializers.ValidationError("You did not provide a valid password")
        user.set_password(password)
        user.save()
        send_email_verification_mail_async(user_id=user.id)
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["userInfo"] = {"email": user.email, "user_type": user.user_type}
        if not user.is_verified:
            raise exceptions.ValidationError("This is user is not verified")
        return token


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context["request"].user
        old_password = data["old_password"]
        new_password = data["new_password"]
        if user:
            if not user.check_password(old_password):
                raise serializers.ValidationError("The old password field is incorrect")
        if old_password == new_password:
            raise serializers.ValidationError(
                "old password and new password must be different"
            )
        return data


class PushNoticationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=100)


class ForgotPasswordSerializer(serializers.Serializer):
    """
    This is used to serializer the email field
    """

    email = serializers.EmailField()

    def validate(self, data):

        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            # raise serializers.ValidationError("User does not exist")
            user = None
        data["user"] = user
        return data


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    token = serializers.CharField(required=True)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["groups", "user_permissions", "is_staff"] + User.get_hidden_fields()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        read_only_fields = (
            "email",
            "user_type",
            "is_verified",
            "is_disabled",
        )
        model = User

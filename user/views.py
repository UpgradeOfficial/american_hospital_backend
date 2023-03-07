import logging

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from core.utils import ExpiringActivationTokenGenerator

from .models import User
from .serializers import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    MyTokenObtainPairSerializer,
    PasswordResetSerializer,
)

# from .tasks import send_to_token_async

logger = logging.getLogger("main")

# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class InitiatePasswordResetView(APIView):
    """
    This API is used to initial a password reset from a user who has forgotten their password.
    It will always return 200 ok
    """

    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.validated_data["user"]
        data = {"message": "Email Has Been sent to the email provided"}
        if user is None:
            return Response(status=status.HTTP_200_OK, data=data)
        user.send_password_reset_mail()
        return Response(status=status.HTTP_200_OK, data=data)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ["post", "options"]

    def post(self, request):
        # Extracting data from request and validating it
        data = request.data
        serializer = PasswordResetSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        User.verify_password_reset(**validated_data)
        return Response(
            status=status.HTTP_200_OK, data={"message": "Password Reset Completed"}
        )


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        password = request.data["new_password"]
        if serializer.is_valid(raise_exception=True):
            self.object.set_password(password)
            self.object.save()
            return Response(
                status=status.HTTP_200_OK, data={"message": "Password changed"}
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST, data={"message": "bad request"}
        )

from django.urls import path

from . import views

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import MyTokenObtainPairView

urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "change_password/", views.ChangePasswordView.as_view(), name="change_password"
    ),
    path(
        "initiate_password_reset/",
        views.InitiatePasswordResetView.as_view(),
        name="initiate_password_reset",
    ),
    path(
        "complete-password-reset/",
        views.PasswordResetView.as_view(),
        name="complete_password_reset",
    ),
    path("confirm_email/", views.ConfirmEmailView.as_view(), name="confirm_email"),
]

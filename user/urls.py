from django.urls import path

from . import views

urlpatterns = [
    path(
        "change_password/", views.ChangePasswordView.as_view(), name="change_password"
    ),
    path(
        "initiate_password_reset/",
        views.InitiatePasswordResetView.as_view(),
        name="initiate_password_reset",
    ),
    path(
        "password-reset/",
        views.PasswordResetView.as_view(),
        name="complete_password_reset",
    ),
    path("confirm_email/", views.ConfirmEmailView.as_view(), name="confirm_email"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.PatientRegistrationView.as_view(), name="register"),
    path(
        "patient/profile-settings/",
        views.PatientProfileDetailsAPIView.as_view(),
        name="profile",
    ),
    path("list/", views.PatientListView.as_view(), name="listpatients"),
]

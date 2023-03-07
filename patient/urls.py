from . import views
from django.urls import path

urlpatterns = [
    path("register", views.PatientRegistrationView.as_view(), name="register"),
    path(
        "patient/profile-settings/",
        views.PatientProfileDetailsAPIView.as_view(),
        name="profile",
    ),
    path("listpatients", views.PatientListView.as_view(), name="listpatients"),
]

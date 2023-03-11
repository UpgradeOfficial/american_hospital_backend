from django.urls import path

from . import views

urlpatterns = [
    path("", views.TestimonialCreateView.as_view(), name="create"),
    path("list/", views.TestimonialListView.as_view(), name="list"),
    path(
        "<uuid:pk>/",
        views.TestimonialRetrieveUpdateDestroyView.as_view(),
        name="detail",
    ),
]

from . import views
from django.urls import path

urlpatterns = [
    path("", views.TestimonialCreateView.as_view(), name="create"),
    path("list/", views.TestimonialListView.as_view(), name="list"),
    path(
        "<uuid:pk>/",
        views.TestimonialRetrieveUpdateDestroyView.as_view(),
        name="detail",
    ),
]

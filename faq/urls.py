from . import views
from django.urls import path


urlpatterns = [
    path("create/", views.FAQCreateView.as_view(), name="create"),
    path("list/", views.FAQListView.as_view(), name="list"),
    path("<uuid:pk>/", views.FAQRetrieveUpdateDelete.as_view(), name="retrieve-update-delete"),
]
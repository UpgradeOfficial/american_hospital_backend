from . import views
from django.urls import path

urlpatterns = [
    path("category/", views.CategoryView.as_view(), name="category"),
    path("news/", views.NewsView.as_view(), name="news"),
]

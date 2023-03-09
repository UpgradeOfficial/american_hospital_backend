from . import views
from django.urls import path

urlpatterns = [
    path("category", views.CategoryView.as_view(), name="create"),
    path("category-list/", views.CategoryListView.as_view(), name="category-list/"),
    path("category/<uuid:pk>", views.CategoryRetrieveView.as_view(), name="category-retrieve"),
    
    path("news/", views.NewsCreateView.as_view(), name="news-create"),
    path("news-list/", views.NewsListView.as_view(), name="news-list"),
    path("<uuid:pk>/", views.NewsRetrieveView.as_view(), name="news-retrieve"),
]

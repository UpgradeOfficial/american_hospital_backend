from django.urls import path

from . import views

urlpatterns = [
    path("category", views.CategoryCreateView.as_view(), name="create_category"),
    path("category-list/", views.CategoryListView.as_view(), name="category-list"),
    path(
        "category/<uuid:pk>",
        views.CategoryRetrieveUpdateDestroyView.as_view(),
        name="category-detail",
    ),
    path("", views.NewsCreateView.as_view(), name="news_create"),
    path("list/", views.NewsListView.as_view(), name="news_list"),
    path(
        "<uuid:pk>/", views.NewsRetrieveUpdateDestroyView.as_view(), name="news_detail"
    ),
]

from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,  # new
    ArticleUpdateView,   # new
    ArticleDeleteView,   # new
    ArticleCreateView,
)

urlpatterns = [
    path("", ArticleListView.as_view(), name="article_list"),  # List of articles
    path("<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),  # Article detail
    path("<int:pk>/edit/", ArticleUpdateView.as_view(), name="article_edit"),  # Edit article
    path("<int:pk>/delete/", ArticleDeleteView.as_view(), name="article_delete"),  # Delete article
    path("new/", ArticleCreateView.as_view(), name="article_new"),
]

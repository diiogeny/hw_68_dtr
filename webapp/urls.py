from django.urls import path
from webapp.views.articles import (
    ArticleListView, ArticleDetailView, ArticleTestView, ArticleCreateView,
    ArticleUpdateView, ArticleDeleteView, article_like, article_dislike)
from webapp.views.comments import (
    CommentListView, CommentDetailView, CommentsCreateView,
    CommentsUpdateView, CommentsDeleteView, comment_like, comment_dislike)

app_name = "webapp"

urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="articles"),
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("articles/add/", ArticleCreateView.as_view(), name="article_add"),
    path("articles/<int:pk>/update/", ArticleUpdateView.as_view(), name="article_update"),
    path("articles/<int:pk>/delete/", ArticleDeleteView.as_view(), name="article_delete"),
    path("articles/<int:pk>/like/", article_like, name="article_like"),
    path("articles/<int:pk>/dislike/", article_dislike, name="article_dislike"),
    path('articles/<int:pk>/test/', ArticleTestView.as_view(), name='article_test'),

    path("articles/<int:article_id>/comments/", CommentListView.as_view(), name="article_comments"),
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="comment_detail"),
    path("comments/<int:pk>/update/", CommentsUpdateView.as_view(), name="comment_update"),
    path("comments/<int:pk>/delete/", CommentsDeleteView.as_view(), name="comment_delete"),
    path("comments/<int:pk>/like/", comment_like, name="comment_like"),
    path("comments/<int:pk>/dislike/", comment_dislike, name="comment_dislike"),
]

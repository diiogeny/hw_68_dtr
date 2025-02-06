from django.urls import path
from webapp.views.articles import *
from webapp.views.comments import *

app_name = "webapp"

urlpatterns = [
    path("articles/", ArticleListCreateView.as_view(), name="articles"),
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("articles/<int:pk>/like/", ArticleLikeAPIView.as_view(), name="article_like"),
    path("articles/<int:pk>/dislike/", ArticleDislikeAPIView.as_view(), name="article_dislike"),
    path("articles/<int:article_id>/comments/", CommentListView.as_view(), name="article_comments"),
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="comment_detail"),
    path("comments/<int:pk>/like/", CommentLikeAPIView.as_view(), name="comment_like"),
    path("comments/<int:pk>/dislike/", CommentDislikeAPIView.as_view(), name="comment_dislike"),
    path("articles/", ArticleListView.as_view(), name="articles"),
]

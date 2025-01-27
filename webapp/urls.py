from django.urls import path
from webapp.views import (
    ArticleListView, ArticleCreateView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView,
    CommentsCreateView, CommentsUpdateView, CommentsDeleteView, TestView
)
from webapp.views.articles import article_like, article_dislike
from webapp.views.comments import comment_like, comment_dislike

app_name = 'webapp'

urlpatterns = [
    path('', ArticleListView.as_view(), name='articles'),
    path('article/add/', ArticleCreateView.as_view(), name='article_add'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('article/<int:pk>/like/', article_like, name='article_like'),
    path('article/<int:pk>/dislike/', article_dislike, name='article_dislike'),
    path('article/<int:pk>/comment/add/', CommentsCreateView.as_view(), name='comment_add'),
    path('comment/<int:pk>/update/', CommentsUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentsDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:pk>/like/', comment_like, name='comment_like'),
    path('comment/<int:pk>/dislike/', comment_dislike, name='comment_dislike'),
    path('article/<int:pk>/test/', TestView.as_view(), name='article_test'),
]

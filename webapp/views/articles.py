from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from webapp.serializers import ArticleSerializer
from django.shortcuts import render
from webapp.models import Article
from webapp.forms import SearchForm
from django.views.generic import ListView

class ArticleListView(ListView):
    model = Article
    template_name = "articles/index.html"
    context_object_name = "articles"

def article_test(request, pk):
    return render(request, "articles/article_test.html", {"pk": pk})

class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleUpdateView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user == self.get_object().author:
            serializer.save()
        else:
            raise permissions.PermissionDenied("Вы можете редактировать только свои публикации.")

class ArticleDeleteView(generics.DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user == instance.author:
            instance.delete()
        else:
            raise permissions.PermissionDenied("Вы можете удалять только свои публикации.")

class ArticleLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)
            article.dislikes.remove(request.user)
        return Response({"likes_count": article.likes.count(), "dislikes_count": article.dislikes.count()})

class ArticleDislikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        if request.user in article.dislikes.all():
            article.dislikes.remove(request.user)
        else:
            article.dislikes.add(request.user)
            article.likes.remove(request.user)
        return Response({"likes_count": article.likes.count(), "dislikes_count": article.dislikes.count()})

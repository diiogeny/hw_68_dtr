from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from webapp.forms import ArticleForm, SearchForm
from webapp.models import Article
from webapp.serializers import ArticleSerializer
import logging
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView



logger = logging.getLogger(__name__)

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/index.html'
    context_object_name = 'articles'
    ordering = ['-created_at']
    paginate_by = 3
    paginate_orphans = 2

    def dispatch(self, request, *args, **kwargs):
        self.search_form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.search_form.is_valid():
            return self.search_form.cleaned_data['search']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(
                Q(title__icontains=self.search_value) |
                Q(author__username__icontains=self.search_value) |
                Q(author__first_name__icontains=self.search_value) |
                Q(author__last_name__icontains=self.search_value)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            context['search_value'] = self.search_value
        return context

class ArticleDetailView(APIView):

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response({"deleted": pk}, status=status.HTTP_204_NO_CONTENT)

class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'articles/article_create.html'
    form_class = ArticleForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'articles/article_update.html'
    form_class = ArticleForm
    model = Article
    permission_required = 'webapp.change_article'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

class ArticleTestView(DetailView):
    model = Article
    template_name = "articles/article_test.html"
    context_object_name = "article"

class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'articles/article_delete.html'
    model = Article
    success_url = reverse_lazy('webapp:articles')
    permission_required = 'webapp.delete_article'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

class ArticleLikeAPIView(APIView):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        if article.is_liked_by(request.user):
            article.likes.remove(request.user)
            liked = False
        else:
            article.like(request.user)
            liked = True
        return Response({"liked": liked, "likes_count": article.likes.count()}, status=status.HTTP_200_OK)

class ArticleDislikeAPIView(APIView):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        if article.is_disliked_by(request.user):
            article.dislikes.remove(request.user)
            disliked = False
        else:
            article.dislike(request.user)
            disliked = True
        return Response({"disliked": disliked, "dislikes_count": article.dislikes.count()}, status=status.HTTP_200_OK)

class TestView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"message": "This is a test!"})

@login_required
def article_like(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.is_liked_by(request.user):
        article.likes.remove(request.user)
        liked = False
    else:
        article.like(request.user)
        liked = True
    return JsonResponse({
        "liked": liked,
        "likes_count": article.likes.count(),
    })

@login_required
def article_dislike(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.is_disliked_by(request.user):
        article.dislikes.remove(request.user)
        disliked = False
    else:
        article.dislike(request.user)
        disliked = True
    return JsonResponse({
        "disliked": disliked,
        "dislikes_count": article.dislikes.count(),
    })



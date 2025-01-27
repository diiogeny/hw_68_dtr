from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import View, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from webapp.forms import ArticleForm, SearchForm
from webapp.models import Article
from django.contrib.auth.decorators import login_required
import logging

class TestView(View):
    def get(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        return JsonResponse({'test': 'test', 'id': f'article_{article.id}', 'comments_count': article.comments.count()})


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/index.html'
    context_object_name = 'articles'
    ordering = ['-created_at']
    paginate_by = 3
    paginate_orphans = 2

    def dispatch(self, request, *args, **kwargs):
        # print(request.user)
        # print(request.user.is_authenticated)
        # print(request.user.is_anonymous)
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


class ArticleDetailView(DetailView):
    template_name = 'articles/article_view.html'
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.order_by('-created_at')
        return context


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

    # def dispatch(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     if not request.user.is_authenticated:
    #         return redirect('accounts:login')
    #     if (not request.user.is_superuser
    #             and not request.user.has_perm('webapp.change_article')
    #             and request.user != self.object.author):
    #         raise PermissionDenied
    #     return super().dispatch(request, *args, **kwargs)


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'articles/article_delete.html'
    model = Article
    success_url = reverse_lazy('webapp:articles')
    permission_required = 'webapp.delete_article'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

logger = logging.getLogger(__name__)

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

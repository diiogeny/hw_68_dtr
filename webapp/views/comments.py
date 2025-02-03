from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from webapp.forms import CommentForm
from webapp.models import Comment, Article
from webapp.serializers import CommentSerializer
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from webapp.models import Comment
from django.views.generic import DetailView


class CommentsCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comments/comment_create.html'
    form_class = CommentForm

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        form.instance.article = article
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:article_detail', kwargs={'pk': self.object.article.pk})

class CommentsUpdateView(PermissionRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_update.html'
    permission_required = 'webapp.change_comment'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('webapp:article_detail', kwargs={'pk': self.object.article.pk})

class CommentsDeleteView(PermissionRequiredMixin, DeleteView):
    model = Comment
    permission_required = 'webapp.delete_comment'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect('webapp:article_detail', pk=self.object.article.pk)

class CommentListAPIView(APIView):

    def get(self, request, article_pk):
        comments = Comment.objects.filter(article_id=article_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentDetailAPIView(APIView):

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response({"deleted": pk}, status=status.HTTP_204_NO_CONTENT)

class CommentLikeAPIView(APIView):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.is_liked_by(request.user):
            comment.likes.remove(request.user)
            liked = False
        else:
            comment.like(request.user)
            liked = True
        return Response({"liked": liked, "likes_count": comment.likes.count()}, status=status.HTTP_200_OK)

class CommentDislikeAPIView(APIView):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.is_disliked_by(request.user):
            comment.dislikes.remove(request.user)
            disliked = False
        else:
            comment.dislike(request.user)
            disliked = True
        return Response({"disliked": disliked, "dislikes_count": comment.dislikes.count()}, status=status.HTTP_200_OK)

class CommentListView(ListView):
    model = Comment
    template_name = "comments/comment_list.html"
    context_object_name = "comments"

class CommentDetailView(DetailView):
    model = Comment
    template_name = "comments/comment_detail.html"
    context_object_name = "comment"

@login_required
def comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.is_liked_by(request.user):
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.like(request.user)
        liked = True
    return JsonResponse({
        "liked": liked,
        "likes_count": comment.likes.count(),
    })

@login_required
def comment_dislike(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.is_disliked_by(request.user):
        comment.dislikes.remove(request.user)
        disliked = False
    else:
        comment.dislike(request.user)
        disliked = True
    return JsonResponse({
        "disliked": disliked,
        "dislikes_count": comment.dislikes.count(),
    })

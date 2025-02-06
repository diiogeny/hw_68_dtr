from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from webapp.models import Comment, Article
from webapp.serializers import CommentSerializer

class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(article_id=self.kwargs['article_id'])

    def perform_create(self, serializer):
        article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        serializer.save(author=self.request.user, article=article)

class CommentDetailView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentUpdateView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user == self.get_object().author:
            serializer.save()
        else:
            raise permissions.PermissionDenied("Вы можете редактировать только свои комментарии.")

class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user == instance.author:
            instance.delete()
        else:
            raise permissions.PermissionDenied("Вы можете удалять только свои комментарии.")

class CommentLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
            comment.dislikes.remove(request.user)
        return Response({"likes_count": comment.likes.count(), "dislikes_count": comment.dislikes.count()})

class CommentDislikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if request.user in comment.dislikes.all():
            comment.dislikes.remove(request.user)
        else:
            comment.dislikes.add(request.user)
            comment.likes.remove(request.user)
        return Response({"likes_count": comment.likes.count(), "dislikes_count": comment.dislikes.count()})

from rest_framework import serializers
from webapp.models.article import Article
from webapp.models.comment import Comment

class ArticleSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislikes.count', read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'likes_count', 'dislikes_count']


class CommentSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislikes.count', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'article', 'text', 'author', 'likes_count', 'dislikes_count']

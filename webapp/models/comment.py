from django.contrib.auth import get_user_model
from django.db import models

from webapp.models import BaseModel

User = get_user_model()


class Comment(BaseModel):
    article = models.ForeignKey('webapp.Article', related_name='comments', on_delete=models.CASCADE,
                                verbose_name='Статья')
    text = models.TextField(max_length=400, verbose_name='Комментарий')
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name='comments',
                               verbose_name='Автор')
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True, verbose_name='Лайки')
    dislikes = models.ManyToManyField(User, related_name='disliked_comments', blank=True, verbose_name='Дизлайки')

    def like(self, user):
        self.likes.add(user)
        self.dislikes.remove(user)

    def dislike(self, user):
        self.dislikes.add(user)
        self.likes.remove(user)

    def is_liked_by(self, user):
        return self.likes.filter(pk=user.pk).exists()

    def is_disliked_by(self, user):
        return self.dislikes.filter(pk=user.pk).exists()

    def __str__(self):
        return self.text[:20]

    class Meta:
        db_table = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

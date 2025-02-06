from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from webapp.models import BaseModel

User = get_user_model()

class Article(BaseModel):
    title = models.CharField(max_length=50, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Контент")
    tags = models.ManyToManyField('webapp.Tag', related_name='articles', blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name='articles', verbose_name='Автор')
    likes = models.ManyToManyField(User, related_name='liked_articles', blank=True, verbose_name='Лайки')
    dislikes = models.ManyToManyField(User, related_name='disliked_articles', blank=True, verbose_name='Дизлайки')

    def like(self, user):
        if self.likes.filter(pk=user.pk).exists():
            self.likes.remove(user)
        else:
            self.likes.add(user)
            self.dislikes.remove(user)

    def dislike(self, user):
        if self.dislikes.filter(pk=user.pk).exists():
            self.dislikes.remove(user)
        else:
            self.dislikes.add(user)
            self.likes.remove(user)

    def is_liked_by(self, user):
        return self.likes.filter(pk=user.pk).exists()

    def is_disliked_by(self, user):
        return self.dislikes.filter(pk=user.pk).exists()

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return f'{self.id}. {self.title}'

    class Meta:
        db_table = 'articles'
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        permissions = [
            ('change_article_tags', 'Менять теги статье')
        ]

    def get_absolute_url(self):
        return reverse('webapp:article_detail', kwargs={'pk': self.pk})

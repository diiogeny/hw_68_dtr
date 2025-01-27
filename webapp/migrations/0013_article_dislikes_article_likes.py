# Generated by Django 5.1.3 on 2025-01-27 08:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_alter_article_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='disliked_articles', to=settings.AUTH_USER_MODEL, verbose_name='Дизлайки'),
        ),
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_articles', to=settings.AUTH_USER_MODEL, verbose_name='Лайки'),
        ),
    ]

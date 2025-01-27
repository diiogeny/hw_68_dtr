from django.db import models

from webapp.models import BaseModel


class Tag(BaseModel):
    name = models.CharField(max_length=31, verbose_name='Тег', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

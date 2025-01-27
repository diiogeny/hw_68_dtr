from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models


def avatar_path(instance, filename):
    return f'avatars/{instance.user.username}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_path, verbose_name='Аватар',
                               validators=[
                                   FileExtensionValidator(['jpg', 'jpeg', 'png'],
                                                          "Можно загружать только следующие файлы 'jpg', 'jpeg', 'png'")
                               ]
                               )

    def __str__(self):
        return self.user.get_full_name() + "'s profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

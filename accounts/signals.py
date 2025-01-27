import os

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from accounts.models import Profile



@receiver(pre_save, sender=Profile)
def my_handler(sender, instance, **kwargs):
    if instance.id:
        old_instance = sender.objects.get(id=instance.id)
        if old_instance.avatar and (not instance.avatar or old_instance.avatar.path != instance.avatar.path ):
            if os.path.exists(old_instance.avatar.path):
                os.remove(old_instance.avatar.path)


@receiver(pre_delete, sender=Profile)
def delete_avatar(sender, instance, **kwargs):
    if instance.avatar and os.path.exists(instance.avatar.path):
        os.remove(instance.avatar.path)


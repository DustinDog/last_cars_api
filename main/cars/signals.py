import os
import shutil
from django.db.models.signals import post_delete
from django.dispatch import receiver
from cars.models import CarImage
from django.conf import settings


@receiver(post_delete, sender=CarImage)
def delete_image_in_folder_media(sender, instance, **kwargs):
    image_folder = f"{settings.MEDIA_ROOT}/{instance.image.name}"
    if os.path.isfile(image_folder):
        os.remove(image_folder)

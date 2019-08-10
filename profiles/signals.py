from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token

from .models import UserRole, Role, UserProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)
        UserProfile.objects.get_or_create(user=instance)
        UserRole.objects.get_or_create(user=instance, role=Role.objects.get(alias='super'))

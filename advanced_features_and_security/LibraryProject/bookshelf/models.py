from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import os

def user_profile_photo_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.id}/profile_photos/{filename}'

class CustomUser(AbstractUser):
    """
    Custom user model with additional fields for user profile information.
    """
    date_of_birth = models.DateField(
        _('date of birth'),
        null=True,
        blank=True,
        help_text=_('The birth date of the user')
    )
    
    profile_photo = models.ImageField(
        _('profile photo'),
        upload_to=user_profile_photo_path,
        null=True,
        blank=True,
        help_text=_('Profile photo of the user')
    )
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.username

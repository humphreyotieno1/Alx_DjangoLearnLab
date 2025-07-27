from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
import os

def user_profile_photo_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.id}/profile_photos/{filename}'

class CustomUserManager(BaseUserManager):
    """Custom user model manager where email is the unique identifier."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

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
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    # Use email as the unique identifier instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username


class Book(models.Model):
    """
    Book model representing a book in the library system.
    Includes custom permissions for book management.
    """
    title = models.CharField(
        _('title'),
        max_length=200,
        help_text=_('The title of the book')
    )
    author = models.CharField(
        _('author'),
        max_length=100,
        help_text=_('The author of the book')
    )
    isbn = models.CharField(
        _('ISBN'),
        max_length=13,
        unique=True,
        help_text=_('13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    )
    published_date = models.DateField(
        _('published date'),
        null=True,
        blank=True
    )
    description = models.TextField(
        _('description'),
        blank=True,
        help_text=_('Brief description of the book')
    )
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')
        permissions = [
            ('can_create', 'Can create book'),
            ('can_edit', 'Can edit book'),
            ('can_delete', 'Can delete book'),
            ('can_view_all', 'Can view all books'),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Override save to ensure custom permissions are created.
        """
        super().save(*args, **kwargs)
        
        # Ensure content type is created for the model
        content_type = ContentType.objects.get_for_model(self.__class__)
        
        # Create custom permissions if they don't exist
        for codename, name in self._meta.permissions:
            Permission.objects.get_or_create(
                codename=codename,
                content_type=content_type,
                defaults={'name': name}
            )

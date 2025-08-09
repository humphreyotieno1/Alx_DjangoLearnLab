"""
This module contains the models for the API. The models are Author and Book.
Author and Book are related by a foreign key, with each Book having one Author.
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Author(models.Model):
    """
    This model represents an author. It has a single field, name, which is a
    string representing the author's name.
    """
    name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        """
        This method returns a string representation of the Author.
        """
        return self.name


class Book(models.Model):
    """
    This model represents a book. It has three fields: title, publication_year,
    and author. The title is a string representing the book's title, the
    publication_year is an integer representing the year the book was published,
    and the author is a foreign key to the Author model.
    """
    title = models.CharField(max_length=100, unique=True, null=False)
    publication_year = models.IntegerField(null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def clean(self):
        """
        This method is used to validate that the publication year is not in the
        future. It raises a ValidationError if the year is in the future.
        """
        if self.publication_year > timezone.now().year:
            raise ValidationError("Publication year cannot be in the future")

    def __str__(self):
        """
        This method returns a string representation of the Book.
        """
        return self.title
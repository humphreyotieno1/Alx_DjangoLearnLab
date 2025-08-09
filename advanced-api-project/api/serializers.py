"""
This module contains the serializers for the API. The serializers are
AuthorSerializer and BookSerializer. AuthorSerializer handles the relationship
between Author and Book by including a field for the related books. The books
field is a StringRelatedField, which means it will be displayed as a string
representation of the related book objects.

BookSerializer includes all fields from the Book model. It also includes a custom
validation method to ensure that the publication year is not in the future.
"""

from rest_framework import serializers
from django.utils import timezone

from .models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.

    This serializer handles the relationship between Author and Book by
    including a field for the related books. The books field is a
    StringRelatedField, which means it will be displayed as a string
    representation of the related book objects.
    """

    books = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        """
        Meta class for the AuthorSerializer.

        This class is used to specify the fields that should be included in
        the serialized data, as well as the model that this serializer should
        be used with.
        """
        fields = ['id', 'name', 'books']
        model = Author

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    This serializer includes all fields from the Book model. It also includes a
    custom validation method to ensure that the publication year is not in the
    future.
    """
    
    class Meta:
        """
        Meta class for the BookSerializer.

        This class is used to specify the fields that should be included in
        the serialized data, as well as the model that this serializer should
        be used with.
        """
        fields = '__all__'
        model = Book
    
    def validate(self, data):
        """
        Custom validation method for the publication_year field.

        This method checks to see if the publication year is in the future. If
        it is, a ValidationError is raised.
        """
        if data['publication_year'] > timezone.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future")
        return data
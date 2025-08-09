"""
Views for the API application.

This module contains the views for handling Book and Author resources,
including CRUD operations, filtering, searching, and ordering.
"""
from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorListCreateView(generics.ListCreateAPIView):
    """
    API view for listing all authors or creating a new author.
    
    - GET: Returns a list of all authors
    - POST: Creates a new author (requires authentication)
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def perform_create(self, serializer):
        """Associate the created author with the current user."""
        serializer.save(user=self.request.user)


class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting an author.
    
    - GET: Returns the author details
    - PUT/PATCH: Updates the author (requires authentication and ownership)
    - DELETE: Deletes the author (requires authentication and ownership)
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'

    def check_object_permissions(self, request, obj):
        """Check if the user has permission to modify the author."""
        super().check_object_permissions(request, obj)
        if request.method not in permissions.SAFE_METHODS and obj.user != request.user:
            self.permission_denied(
                request,
                message="You do not have permission to perform this action.",
                code=status.HTTP_403_FORBIDDEN
            )


class BookListView(generics.ListAPIView):
    """
    API view for listing and searching books.
    
    Supports:
    - Filtering by author and publication year
    - Searching by title and author name
    - Ordering by title, publication year, and author name
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filter configuration
    filterset_fields = {
        'author': ['exact'],
        'publication_year': ['exact', 'gt', 'lt', 'gte', 'lte'],
    }
    
    # Search configuration
    search_fields = ['title', 'author__name']
    
    # Ordering configuration
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving a single book by ID.
    
    - GET: Returns the book details
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'


class BookCreateView(generics.CreateAPIView):
    """
    API view for creating a new book.
    
    - POST: Creates a new book (requires authentication)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Associate the created book with the current user."""
        serializer.save(user=self.request.user)


class BookUpdateView(generics.UpdateAPIView):
    """
    API view for updating a book.
    
    - PUT/PATCH: Updates the book (requires authentication and ownership)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def check_object_permissions(self, request, obj):
        """Check if the user has permission to modify the book."""
        super().check_object_permissions(request, obj)
        if obj.user != request.user:
            self.permission_denied(
                request,
                message="You do not have permission to perform this action.",
                code=status.HTTP_403_FORBIDDEN
            )


class BookDeleteView(generics.DestroyAPIView):
    """
    API view for deleting a book.
    
    - DELETE: Deletes the book (requires authentication and ownership)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def check_object_permissions(self, request, obj):
        """Check if the user has permission to delete the book."""
        super().check_object_permissions(request, obj)
        if obj.user != request.user:
            self.permission_denied(
                request,
                message="You do not have permission to perform this action.",
                code=status.HTTP_403_FORBIDDEN
            )
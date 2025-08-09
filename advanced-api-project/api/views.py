# generic views
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework import filters

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# views

class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def check_object_permissions(self, request, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class BookListView(generics.ListAPIView):
    """
    API view for listing and searching books.
    
    Supports:
    - Filtering by author ID and publication year
    - Searching by title and author name
    - Ordering by title, publication year, and author name
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Configure filter backends
    filter_backends = [
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    
    # Define filter fields
    filterset_fields = {
        'author': ['exact'],
        'publication_year': ['exact', 'gt', 'lt', 'gte', 'lte'],
    }
    
    # Define search fields
    search_fields = ['title', 'author__name']
    
    # Define ordering fields
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering
    
    def get_queryset(self):
        """
        Optionally filter the books by author if provided in query params.
        This is in addition to the filtering provided by DjangoFilterBackend.
        """
        queryset = super().get_queryset()
        author_id = self.request.query_params.get('author_id')
        if author_id is not None:
            queryset = queryset.filter(author_id=author_id)
        return queryset

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def check_object_permissions(self, request, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
    
class BookDeleteView(generics.DeleteAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

class BookDestroyView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def check_object_permissions(self, request, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
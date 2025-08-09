from django.urls import path
from .views import BookListCreateView, BookDetailView, AuthorListCreateView, AuthorDetailView, BookUpdateView, BookDeleteView, BookDestroyView, BookCreateView

urlpatterns = [
    path('books/', BookListCreateView.as_view()),
    path('books/<int:pk>/', BookDetailView.as_view()),
    path('authors/', AuthorListCreateView.as_view()),
    path('authors/<int:pk>/', AuthorDetailView.as_view()),
    path('books/<int:pk>/update/', BookUpdateView.as_view()),
    path('books/delete/', BookDeleteView.as_view()),
    path('books/destroy/', BookDestroyView.as_view()),
    path('books/create/', BookCreateView.as_view()),
    path('books/update/', BookUpdateView.as_view()),
]

from django.urls import path
from .views import BookListCreateView, BookDetailView, AuthorListCreateView, AuthorDetailView, BookUpdateView, BookDeleteView, BookDestroyView

urlpatterns = [
    path('books/', BookListCreateView.as_view()),
    path('books/<int:pk>/', BookDetailView.as_view()),
    path('authors/', AuthorListCreateView.as_view()),
    path('authors/<int:pk>/', AuthorDetailView.as_view()),
    path('books/<int:pk>/update/', BookUpdateView.as_view()),
    path('books/<int:pk>/delete/', BookDeleteView.as_view()),
    path('books/<int:pk>/destroy/', BookDestroyView.as_view()),
]

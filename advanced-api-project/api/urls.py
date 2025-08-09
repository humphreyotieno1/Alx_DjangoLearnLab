"""
URL configuration for the API application.

This module maps URL patterns to views for the Book and Author resources.
"""
from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Author endpoints
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorRetrieveUpdateDestroyView.as_view(), 
         name='author-detail'),
    
    # Book endpoints
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
]
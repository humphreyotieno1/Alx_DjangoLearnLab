#!/usr/bin/env python
"""
This script demonstrates various query operations for the Library Management System.
It includes examples of querying relationships between models.
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def get_books_by_author(author_name):
    """
    Query all books written by a specific author.
    
    Args:
        author_name (str): Name of the author to search for
        
    Returns:
        QuerySet: All books by the specified author, ordered by publication year
    """
    try:
        books = Book.objects.filter(
            author__name__icontains=author_name
        ).order_by('publication_year')
        
        if books.exists():
            print(f"\nBooks by {author_name}:")
            for book in books:
                print(f"- {book.title} ({book.publication_year})")
        else:
            print(f"No books found for author: {author_name}")
            
        return books
    except Exception as e:
        print(f"Error finding books by author: {e}")
        return Book.objects.none()

def get_books_in_library(library_name):
    """
    List all books available in a specific library.
    
    Args:
        library_name (str): Name of the library
        
    Returns:
        QuerySet: All books in the specified library, ordered by title
    """
    try:
        library = Library.objects.get(name__iexact=library_name)
        books = library.books.all().order_by('title')
        
        if books.exists():
            print(f"\nBooks available in {library_name} library:")
            for book in books:
                print(f"- {book.title} by {book.author.name}")
        else:
            print(f"No books found in {library_name} library")
            
        return books
    except Library.DoesNotExist:
        print(f"Library not found: {library_name}")
        return Book.objects.none()
    except Exception as e:
        print(f"Error finding books in library: {e}")
        return Book.objects.none()

def get_librarian_for_library(library_name):
    """
    Retrieve the librarian for a specific library.
    
    Args:
        library_name (str): Name of the library
        
    Returns:
        Librarian: The librarian object for the specified library, or None if not found
    """
    try:
        library = Library.objects.get(name__iexact=library_name)
        librarian = Librarian.objects.filter(library=library).first()
        
        if librarian:
            print(f"\nLibrarian for {library_name}:")
            print(f"- {librarian.name}")
        else:
            print(f"No librarian found for {library_name}")
            
        return librarian
    except Library.DoesNotExist:
        print(f"Library not found: {library_name}")
        return None
    except Exception as e:
        print(f"Error finding librarian: {e}")
        return None

def main():
    """
    Main function to demonstrate the query functions.
    """
    print("Library Management System - Sample Queries")
    print("=" * 40)
    
    # Example 1: Get books by an author
    get_books_by_author("J.K. Rowling")
    
    # Example 2: Get books in a library
    get_books_in_library("Central Library")
    
    # Example 3: Get librarian for a library
    get_librarian_for_library("Central Library")

if __name__ == "__main__":
    main()

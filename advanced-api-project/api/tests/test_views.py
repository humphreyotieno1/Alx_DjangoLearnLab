"""
Tests for the Book API views.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Author, Book

BOOKS_URL = reverse('book-list')


def create_author(name='Test Author'):
    """Create and return a sample author."""
    return Author.objects.create(name=name)


def create_book(author, **params):
    """Create and return a sample book."""
    defaults = {
        'title': 'Sample Book Title',
        'publication_year': 2020,
    }
    defaults.update(params)
    return Book.objects.create(author=author, **defaults)


class PublicBookAPITests(TestCase):
    """Test the publicly available book API."""

    def setUp(self):
        self.client = APIClient()
        self.author = create_author()

    def test_retrieve_books(self):
        """Test retrieving a list of books."""
        create_book(author=self.author, title='Book 1', publication_year=2020)
        create_book(author=self.author, title='Book 2', publication_year=2021)

        res = self.client.get(BOOKS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)
        self.assertEqual(res.data['results'][0]['title'], 'Book 1')
        self.assertEqual(res.data['results'][1]['title'], 'Book 2')

    def test_filter_books_by_author(self):
        """Test filtering books by author."""
        author2 = create_author(name='Second Author')
        book1 = create_book(author=self.author, title='Book 1')
        create_book(author=author2, title='Book 2')

        res = self.client.get(BOOKS_URL, {'author': self.author.id})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0]['title'], book1.title)

    def test_filter_books_by_publication_year(self):
        """Test filtering books by publication year."""
        book1 = create_book(author=self.author, title='Book 1', publication_year=2020)
        create_book(author=self.author, title='Book 2', publication_year=2021)

        res = self.client.get(BOOKS_URL, {'publication_year': 2020})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0]['title'], book1.title)

    def test_search_books(self):
        """Test searching books by title and author name."""
        create_book(author=self.author, title='Django for Beginners', publication_year=2020)
        create_book(author=self.author, title='Python Cookbook', publication_year=2021)
        author2 = create_author(name='Jane Smith')
        create_book(author=author2, title='Advanced Python', publication_year=2022)

        # Search by title
        res = self.client.get(BOOKS_URL, {'search': 'Django'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0]['title'], 'Django for Beginners')

        # Search by author name
        res = self.client.get(BOOKS_URL, {'search': 'Jane'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0]['title'], 'Advanced Python')

    def test_ordering_books(self):
        """Test ordering books by different fields."""
        book1 = create_book(author=self.author, title='Book B', publication_year=2021)
        book2 = create_book(author=self.author, title='Book A', publication_year=2020)

        # Order by title ascending
        res = self.client.get(BOOKS_URL, {'ordering': 'title'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'][0]['title'], book2.title)  # Book A
        self.assertEqual(res.data['results'][1]['title'], book1.title)  # Book B

        # Order by publication year descending
        res = self.client.get(BOOKS_URL, {'ordering': '-publication_year'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'][0]['publication_year'], book1.publication_year)  # 2021
        self.assertEqual(res.data['results'][1]['publication_year'], book2.publication_year)  # 2020


class PrivateBookAPITests(TestCase):
    """Test the authorized user book API."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.author = create_author()

    def test_create_book_successful(self):
        """Test creating a new book."""
        payload = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        res = self.client.post(BOOKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(id=res.data['id'])
        self.assertEqual(book.title, payload['title'])
        self.assertEqual(book.author, self.author)

    def test_create_book_invalid(self):
        """Test creating a new book with invalid payload."""
        payload = {'title': ''}
        res = self.client.post(BOOKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

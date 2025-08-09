"""
Tests for the API views.

This module contains test cases for all the API endpoints.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Author, Book

User = get_user_model()


def create_user(username='testuser', password='testpass123'):
    """Create and return a test user."""
    return User.objects.create_user(username=username, password=password)


def create_author(user, name='Test Author', bio='Test Bio'):
    """Create and return a test author."""
    return Author.objects.create(user=user, name=name, bio=bio)


def create_book(author, title='Test Book', description='Test Description', publication_year=2023):
    """Create and return a test book."""
    return Book.objects.create(
        user=author.user,
        author=author,
        title=title,
        description=description,
        publication_year=publication_year
    )


class PublicApiTests(APITestCase):
    """Test unauthenticated API access."""

    def setUp(self):
        self.user = create_user()
        self.author = create_author(self.user)
        self.book = create_book(self.author)

    def test_author_list_unauthorized(self):
        """Test retrieving authors as an unauthenticated user."""
        url = reverse('api:author-list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_book_list_unauthorized(self):
        """Test retrieving books as an unauthenticated user."""
        url = reverse('api:book-list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_author_create_unauthorized(self):
        """Test that creating an author requires authentication."""
        url = reverse('api:author-list')
        payload = {'name': 'New Author', 'bio': 'New Bio'}
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAuthorApiTests(APITestCase):
    """Test the authorized user Author API."""

    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)
        self.author = create_author(self.user)

    def test_create_author(self):
        """Test creating an author."""
        url = reverse('api:author-list')
        payload = {'name': 'J.R.R. Tolkien', 'bio': 'Author of Lord of the Rings'}
        res = self.client.post(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        author = Author.objects.get(id=res.data['id'])
        self.assertEqual(author.name, payload['name'])
        self.assertEqual(author.bio, payload['bio'])
        self.assertEqual(author.user, self.user)

    def test_retrieve_author(self):
        """Test retrieving an author."""
        url = reverse('api:author-detail', args=[self.author.id])
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], self.author.name)
        self.assertEqual(res.data['bio'], self.author.bio)

    def test_update_author(self):
        """Test updating an author."""
        payload = {'name': 'Updated Name', 'bio': 'Updated Bio'}
        url = reverse('api:author-detail', args=[self.author.id])
        res = self.client.put(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.name, payload['name'])
        self.assertEqual(self.author.bio, payload['bio'])

    def test_delete_author(self):
        """Test deleting an author."""
        url = reverse('api:author-detail', args=[self.author.id])
        res = self.client.delete(url)
        
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Author.objects.filter(id=self.author.id).exists())


class PrivateBookApiTests(APITestCase):
    """Test the authorized user Book API."""

    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)
        self.author = create_author(self.user)
        self.book = create_book(self.author)

    def test_create_book(self):
        """Test creating a book."""
        url = reverse('api:book-create')
        payload = {
            'title': 'The Hobbit',
            'description': 'A book about a hobbit',
            'publication_year': 1937,
            'author': self.author.id
        }
        res = self.client.post(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(id=res.data['id'])
        self.assertEqual(book.title, payload['title'])
        self.assertEqual(book.author.id, payload['author'])
        self.assertEqual(book.user, self.user)

    def test_retrieve_book(self):
        """Test retrieving a book."""
        url = reverse('api:book-detail', args=[self.book.id])
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], self.book.title)
        self.assertEqual(res.data['author'], self.author.id)

    def test_update_book(self):
        """Test updating a book."""
        payload = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'publication_year': 2000,
            'author': self.author.id
        }
        url = reverse('api:book-update', args=[self.book.id])
        res = self.client.put(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, payload['title'])
        self.assertEqual(self.book.publication_year, payload['publication_year'])

    def test_delete_book(self):
        """Test deleting a book."""
        url = reverse('api:book-delete', args=[self.book.id])
        res = self.client.delete(url)
        
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())


class BookFilteringTests(APITestCase):
    """Test the book filtering, searching, and ordering."""

    def setUp(self):
        self.user = create_user()
        self.author1 = create_author(self.user, name='J.K. Rowling')
        self.author2 = create_author(self.user, name='George R.R. Martin')
        
        self.book1 = create_book(
            self.author1, 
            title='Harry Potter', 
            description='Wizard school',
            publication_year=1997
        )
        self.book2 = create_book(
            self.author2,
            title='A Game of Thrones',
            description='Game of Thrones book 1',
            publication_year=1996
        )
        self.book3 = create_book(
            self.author1,
            title='The Hobbit',
            description='Hobbit adventure',
            publication_year=1937
        )

    def test_filter_by_author(self):
        """Test filtering books by author."""
        url = f"{reverse('api:book-list')}?author={self.author1.id}"
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)  # 2 books by author1
        self.assertEqual(res.data[0]['author'], self.author1.id)
        self.assertEqual(res.data[1]['author'], self.author1.id)

    def test_filter_by_publication_year(self):
        """Test filtering books by publication year."""
        url = f"{reverse('api:book-list')}?publication_year__gt=1990"
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)  # 2 books after 1990

    def test_search_books(self):
        """Test searching books by title and author name."""
        url = f"{reverse('api:book-list')}?search=Harry"
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], 'Harry Potter')

    def test_order_books(self):
        """Test ordering books by different fields."""
        # Order by title (ascending)
        url = f"{reverse('api:book-list')}?ordering=title"
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['title'], 'A Game of Thrones')
        self.assertEqual(res.data[1]['title'], 'Harry Potter')
        self.assertEqual(res.data[2]['title'], 'The Hobbit')
        
        # Order by publication_year (descending)
        url = f"{reverse('api:book-list')}?ordering=-publication_year"
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['title'], 'Harry Potter')  # 1997
        self.assertEqual(res.data[1]['title'], 'A Game of Thrones')  # 1996
        self.assertEqual(res.data[2]['title'], 'The Hobbit')  # 1937

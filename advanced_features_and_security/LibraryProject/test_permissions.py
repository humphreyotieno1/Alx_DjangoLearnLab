#!/usr/bin/env python
"""
Test script to verify Django permissions and groups functionality.
Run this script using: python manage.py shell < test_permissions.py
"""
import os
import sys
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book, Author

def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*50)
    print(f" {text} ".center(50, '='))
    print("="*50)

def setup_test_environment():
    """Set up test users and groups if they don't exist."""
    User = get_user_model()
    
    # Create or get groups
    viewer_group, _ = Group.objects.get_or_create(name='Viewers')
    editor_group, _ = Group.objects.get_or_create(name='Editors')
    admin_group, _ = Group.objects.get_or_create(name='Admins')
    
    # Create test users if they don't exist
    users = {
        'viewer': User.objects.get_or_create(
            username='test_viewer',
            defaults={'email': 'viewer@example.com', 'password': 'testpass123'}
        )[0],
        'editor': User.objects.get_or_create(
            username='test_editor',
            defaults={'email': 'editor@example.com', 'password': 'testpass123'}
        )[0],
        'admin': User.objects.get_or_create(
            username='test_admin',
            defaults={'email': 'admin@example.com', 'password': 'testpass123', 'is_staff': True}
        )[0],
    }
    
    # Set passwords
    for user in users.values():
        user.set_password('testpass123')
        user.save()
    
    # Add users to groups
    users['viewer'].groups.add(viewer_group)
    users['editor'].groups.add(editor_group)
    users['admin'].groups.add(admin_group)
    
    # Create a test author if none exists
    author, _ = Author.objects.get_or_create(
        name='Test Author',
        defaults={'bio': 'A test author for permission testing'}
    )
    
    # Create a test book if none exists
    book, _ = Book.objects.get_or_create(
        title='Test Book',
        author=author,
        publication_year=2023,
        created_by=users['admin'],
        last_modified_by=users['admin']
    )
    
    return users, book

def test_permissions(users, book):
    """Test permissions for different user roles."""
    User = get_user_model()
    
    # Test viewer permissions
    print_header("TESTING VIEWER PERMISSIONS")
    viewer = users['viewer']
    print(f"Testing permissions for {viewer.username} (Viewer)")
    print(f"Can view books: {viewer.has_perm('relationship_app.can_view_book')}")
    print(f"Can create books: {viewer.has_perm('relationship_app.can_create_book')}")
    print(f"Can edit books: {viewer.has_perm('relationship_app.can_edit_book')}")
    print(f"Can delete books: {viewer.has_perm('relationship_app.can_delete_book')}")
    
    # Test editor permissions
    print_header("TESTING EDITOR PERMISSIONS")
    editor = users['editor']
    print(f"Testing permissions for {editor.username} (Editor)")
    print(f"Can view books: {editor.has_perm('relationship_app.can_view_book')}")
    print(f"Can create books: {editor.has_perm('relationship_app.can_create_book')}")
    print(f"Can edit books: {editor.has_perm('relationship_app.can_edit_book')}")
    print(f"Can delete books: {editor.has_perm('relationship_app.can_delete_book')}")
    
    # Test admin permissions
    print_header("TESTING ADMIN PERMISSIONS")
    admin = users['admin']
    print(f"Testing permissions for {admin.username} (Admin)")
    print(f"Can view books: {admin.has_perm('relationship_app.can_view_book')}")
    print(f"Can create books: {admin.has_perm('relationship_app.can_create_book')}")
    print(f"Can edit books: {admin.has_perm('relationship_app.can_edit_book')}")
    print(f"Can delete books: {admin.has_perm('relationship_app.can_delete_book')}")

def test_book_operations(users, book):
    """Test book operations with different user roles."""
    print_header("TESTING BOOK OPERATIONS")
    
    # Test viewer trying to edit a book (should fail)
    viewer = users['viewer']
    print(f"\n{viewer.username} (Viewer) trying to edit a book:")
    try:
        book.title = "Modified by Viewer"
        book.save(update_fields=['title'])
        print("  - SUCCESS: Viewer was able to edit a book (UNEXPECTED)")
    except Exception as e:
        print(f"  - PASS: Viewer cannot edit a book: {str(e)}")
    
    # Test editor editing a book (should succeed)
    editor = users['editor']
    print(f"\n{editor.username} (Editor) editing a book:")
    try:
        original_title = book.title
        book.title = "Modified by Editor"
        book.last_modified_by = editor
        book.save(update_fields=['title', 'last_modified_by'])
        print(f"  - SUCCESS: Editor edited book title to: {book.title}")
        # Revert the change
        book.title = original_title
        book.save(update_fields=['title'])
    except Exception as e:
        print(f"  - FAIL: Editor could not edit book: {str(e)}")
    
    # Test admin deleting a book (should succeed)
    admin = users['admin']
    print(f"\n{admin.username} (Admin) deleting a book:")
    try:
        book_pk = book.pk
        book.delete()
        print(f"  - SUCCESS: Admin deleted book with ID {book_pk}")
        # Recreate the book for further testing
        book = Book.objects.create(
            title='Test Book',
            author=Author.objects.first(),
            publication_year=2023,
            created_by=admin,
            last_modified_by=admin
        )
    except Exception as e:
        print(f"  - FAIL: Admin could not delete book: {str(e)}")

if __name__ == "__main__":
    print("Setting up test environment...")
    users, book = setup_test_environment()
    
    print("\n" + "="*50)
    print(" STARTING PERMISSION TESTS ".center(50, '='))
    print("="*50)
    
    test_permissions(users, book)
    test_book_operations(users, book)
    
    print("\n" + "="*50)
    print(" PERMISSION TESTS COMPLETED ".center(50, '='))
    print("="*50)
    print("\nTest users created with password 'testpass123':")
    for role, user in users.items():
        print(f"- {role}: {user.username} (email: {user.email})")
    print("\nYou can now log in to the admin interface to verify the setup.")

# Django Permissions and Groups Guide

This document explains the permission and group system implemented in the Library Management application.

## Overview

The application uses Django's built-in authentication system with custom permissions and groups to control access to different parts of the application. The system includes three main groups with different permission levels: Viewers, Editors, and Admins.

## Groups and Permissions

### 1. Viewers Group
- **Permissions:**
  - `can_view_book` - View book details
- **Description:**
  - Can view the list of books and their details
  - Cannot make any changes to the book records

### 2. Editors Group
- **Permissions:**
  - `can_view_book` - View book details
  - `can_create_book` - Add new books
  - `can_edit_book` - Modify existing books
- **Description:**
  - Can view all books
  - Can add new books
  - Can edit existing books
  - Cannot delete books

### 3. Admins Group
- **Permissions:**
  - `can_view_book` - View book details
  - `can_create_book` - Add new books
  - `can_edit_book` - Modify existing books
  - `can_delete_book` - Delete books
- **Description:**
  - Full access to all book-related operations
  - Can perform all CRUD operations on books

## How Permissions are Enforced

### In Views
Permissions are enforced in views using Django's built-in decorators and methods:

1. **Function-based views:**
   ```python
   from django.contrib.auth.decorators import permission_required
   
   @login_required
   @permission_required('relationship_app.can_edit_book', raise_exception=True)
   def edit_book(request, pk):
       # View logic here
   ```

2. **Class-based views:**
   ```python
   from django.contrib.auth.mixins import PermissionRequiredMixin
   
   class BookUpdateView(PermissionRequiredMixin, UpdateView):
       permission_required = 'relationship_app.can_edit_book'
       # View logic here
   ```

3. **Template-level checks:**
   ```html
   {% if perms.relationship_app.can_edit_book %}
       <a href="{% url 'edit_book' book.id %}" class="btn btn-warning">Edit</a>
   {% endif %}
   ```

### In Templates
Permissions can be checked directly in templates using the `perms` template variable:

```html
{% if perms.relationship_app.can_delete_book %}
    <button class="btn btn-danger">Delete</button>
{% endif %}
```

## Setting Up a New User with Permissions

1. **Create a new user:**
   ```bash
   python manage.py createsuperuser
   ```

2. **Add user to a group (Django Admin):**
   - Log in to the Django admin interface
   - Go to "Groups"
   - Select a group (Viewers, Editors, or Admins)
   - Add the user to the desired group

3. **Or programmatically:**
   ```python
   from django.contrib.auth.models import User, Group
   
   user = User.objects.get(username='username')
   group = Group.objects.get(name='Editors')
   user.groups.add(group)
   ```

## Custom Permissions

Custom permissions are defined in the `Book` model's `Meta` class:

```python
class Book(models.Model):
    # Model fields here
    
    class Meta:
        permissions = [
            ("can_view_book", "Can view book details"),
            ("can_create_book", "Can create book"),
            ("can_edit_book", "Can edit book"),
            ("can_delete_book", "Can delete book"),
        ]
```

## Testing Permissions

To test if permissions are working correctly:

1. Log in as a user with Viewer permissions and verify you can only view books
2. Log in as an Editor and verify you can add and edit books but not delete them
3. Log in as an Admin and verify you have full access to all book operations

## Troubleshooting

- **Permission Denied Errors:** Ensure the user is logged in and has the required permissions
- **Missing Permissions:** Run `python manage.py migrate` to ensure all permissions are created
- **Group Permissions Not Applying:** Check that the user is added to the correct group and that the group has the required permissions

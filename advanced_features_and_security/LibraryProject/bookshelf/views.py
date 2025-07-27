from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Book

@login_required
def book_list(request):
    """
    View to list all books. Requires login.
    Users with 'can_view_all' permission can see all books.
    Regular users only see books they've created.
    """
    if request.user.has_perm('bookshelf.can_view_all'):
        books = Book.objects.all()
    else:
        books = Book.objects.filter(created_by=request.user)
    
    context = {
        'books': books,
        'can_create': request.user.has_perm('bookshelf.can_create'),
        'can_edit': request.user.has_perm('bookshelf.can_edit'),
        'can_delete': request.user.has_perm('bookshelf.can_delete')
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Handle AJAX requests
        data = [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'published_date': book.published_date.strftime('%Y-%m-%d') if book.published_date else None,
            'description': book.description
        } for book in books]
        return JsonResponse({'books': data})
    
    return render(request, 'bookshelf/book_list.html', context)

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    View to create a new book.
    Requires 'can_create' permission.
    """
    if request.method == 'POST':
        try:
            # Process form data and create book
            book = Book.objects.create(
                title=request.POST.get('title'),
                author=request.POST.get('author'),
                isbn=request.POST.get('isbn'),
                published_date=request.POST.get('published_date') or None,
                description=request.POST.get('description', ''),
                created_by=request.user
            )
            messages.success(request, 'Book created successfully!')
            return redirect('bookshelf:book_list')
        except Exception as e:
            messages.error(request, f'Error creating book: {str(e)}')
    
    return render(request, 'bookshelf/book_form.html')

@permission_required('bookshelf.can_delete', raise_exception=True)
@require_http_methods(['POST'])
def book_delete(request, book_id):
    """
    View to delete a book.
    Requires 'can_delete' permission and POST method.
    """
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, 'Book deleted successfully!')
    return redirect('bookshelf:book_list')

def raise_exception(request):
    """
    Utility view to raise a permission denied exception.
    Useful for testing permission handling.
    """
    raise PermissionDenied("You don't have permission to access this page.")

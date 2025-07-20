from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Library
from .models import Book
from .models import Author
from .models import UserProfile
from .forms import BookForm, LibraryForm, UserRegisterForm, UserProfileForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth import authenticate

UserCreationForm()

@require_http_methods(["POST"])
@csrf_exempt
def add_author(request):
    """
    Handle AJAX request to add a new author.
    Returns JSON response with the new author's data or error message.
    """
    try:
        # Print request body for debugging
        print("Request body:", request.body)
        
        # Try to parse JSON data
        try:
            if request.body:
                data = json.loads(request.body)
            else:
                data = request.POST.dict() or {}
        except json.JSONDecodeError:
            # If JSON parsing fails, try to get data from POST
            data = request.POST.dict() or {}
        
        name = data.get('name', '').strip()
        
        print("Author name:", name)  # Debugging
        
        if not name:
            return JsonResponse({
                'success': False, 
                'error': 'Author name is required'
            }, status=400)
            
        # Create the author
        author = Author.objects.create(name=name)
        
        print("Author created:", author)  # Debugging
        
        return JsonResponse({
            'success': True, 
            'id': author.id, 
            'name': author.name,
            'text': str(author)  # For Select2
        })
    except Exception as e:
        import traceback
        print("Error in add_author:")
        print(traceback.format_exc())
        return JsonResponse({
            'success': False, 
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)

# Authentication Views
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        # Get the next URL from the request
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
            
        # Default role-based redirection
        if hasattr(self.request.user, 'userprofile'):
            if self.request.user.userprofile.role == 'Admin':
                return reverse_lazy('relationship_app:admin_view')
            elif self.request.user.userprofile.role == 'Librarian':
                return reverse_lazy('relationship_app:librarian_view')
        
        # Default fallback
        return reverse_lazy('relationship_app:home')

class CustomLogoutView(LogoutView):
    next_page = 'relationship_app:login'

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            # Create user profile with default role 'Member'
            UserProfile.objects.create(user=user, role='Member')
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please log in.')
            return redirect('relationship_app:login')
    else:
        form = UserRegisterForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Role-based access test functions
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Role-based Views
@login_required
def admin_view(request):
    if not is_admin(request.user):
        messages.warning(request, 'You do not have permission to access this page.')
        return redirect('relationship_app:home')
    return render(request, 'relationship_app/admin_view.html')

@login_required
def librarian_view(request):
    if not is_librarian(request.user):
        messages.warning(request, 'You do not have permission to access this page.')
        return redirect('relationship_app:home')
    return render(request, 'relationship_app/librarian_view.html')

@login_required
def member_view(request):
    if not is_member(request.user):
        messages.warning(request, 'You do not have permission to access this page.')
        return redirect('relationship_app:home')
    return render(request, 'relationship_app/member_view.html')

# Book Views
@login_required
def book_list(request):
    # Get all books with related authors
    books = Book.objects.select_related('author').order_by('title')
    
    # Get all authors for the dropdown
    authors = Author.objects.all().order_by('name')
    
    # Handle search
    search_query = request.GET.get('search', '')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__name__icontains=search_query) |
            Q(publication_year__icontains=publication_year)
        )
    
    # Handle pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(books, 10)  # Show 10 books per page
    
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    
    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            'books': [{
                'id': book.id,
                'title': book.title,
                'author': book.author.name,
                'publication_year': book.publication_year,
                'published_date': book.published_date.strftime('%b %d, %Y') if book.published_date else ''
            } for book in books],
            'has_next': books.has_next(),
            'has_previous': books.has_previous(),
            'page_number': books.number,
            'num_pages': paginator.num_pages,
            'count': paginator.count
        }
        return JsonResponse(data)
    
    return render(request, 'relationship_app/books/list_books.html', {
        'books': books,
        'authors': authors
    })

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'relationship_app/book_detail.html'

@login_required
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

@require_POST
@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    form = BookForm(request.POST)
    if form.is_valid():
        book = form.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'id': book.id,
                'title': book.title,
                'author': book.author.name,
                'publication_year': book.publication_year,
                'published_date': book.published_date.strftime('%b %d, %Y') if book.published_date else ''
            })
        messages.success(request, 'Book added successfully!')
        return redirect('relationship_app:book_list')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'error': 'Invalid form data',
            'errors': form.errors
        }, status=400)
        
    return render(request, 'relationship_app/books/list_books.html', {
        'form': form,
        'books': Book.objects.all().order_by('title')
    })

@require_http_methods(["POST"])
@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST, instance=book)
    
    if form.is_valid():
        book = form.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'id': book.id,
                'title': book.title,
                'author': book.author.name,
                'publication_year': book.publication_year,
                'published_date': book.published_date.strftime('%b %d, %Y') if book.published_date else ''
            })
        messages.success(request, 'Book updated successfully!')
        return redirect('relationship_app:book_list')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'error': 'Invalid form data',
            'errors': form.errors
        }, status=400)
        
    return render(request, 'relationship_app/books/list_books.html', {
        'form': form,
        'books': Book.objects.all().order_by('title')
    })

@require_POST
@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book_id = book.id
    book.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'id': book_id
        })
        
    messages.success(request, 'Book deleted successfully!')
    return redirect('relationship_app:book_list')

@require_POST
@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def bulk_delete_books(request):
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    
    try:
        book_ids = request.POST.getlist('ids[]') or json.loads(request.body).get('ids', [])
        if not book_ids:
            return JsonResponse({'success': False, 'error': 'No books selected'}, status=400)
        
        # Delete books and get count
        count, _ = Book.objects.filter(id__in=book_ids).delete()
        
        return JsonResponse({
            'success': True,
            'count': count
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# Library Views
class LibraryListView(LoginRequiredMixin, ListView):
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'

class LibraryDetailView(LoginRequiredMixin, DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'

@login_required
def add_library(request):
    if request.method == 'POST':
        form = LibraryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Library added successfully!')
            return redirect('relationship_app:library_list')
    else:
        form = LibraryForm()
    return render(request, 'relationship_app/library_detail.html', {'form': form, 'title': 'Add Library'})

@login_required
def edit_library(request, pk):
    library = get_object_or_404(Library, pk=pk)
    if request.method == 'POST':
        form = LibraryForm(request.POST, instance=library)
        if form.is_valid():
            form.save()
            messages.success(request, 'Library updated successfully!')
            return redirect('relationship_app:library_list')
    else:
        form = LibraryForm(instance=library)
    return render(request, 'relationship_app/library_detail.html', {'form': form, 'title': 'Edit Library'})

@login_required
def delete_library(request, pk):
    library = get_object_or_404(Library, pk=pk)
    if request.method == 'POST':
        library.delete()
        messages.success(request, 'Library deleted successfully!')
        return redirect('library_list')
    return render(request, 'relationship_app/library_confirm_delete.html', {'library': library})

# Home View
@login_required
def home(request):
    if is_admin(request.user):
        return redirect('relationship_app:admin_view')
    elif is_librarian(request.user):
        return redirect('relationship_app:librarian_view')
    else:
        return redirect('relationship_app:member_view')
    
# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('relationship_app:login')


# User Profile View
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('relationship_app:profile')
    else:
        user_form = UserRegisterForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'relationship_app/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

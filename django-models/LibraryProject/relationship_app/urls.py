from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import list_books


app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
    # Home and Profile
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    
    # AJAX Endpoints
    path('authors/add/', views.add_author, name='add_author'),
    
    # Role-based Views
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
    
    # Book URLs
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    path('books/bulk-delete/', views.bulk_delete_books, name='bulk_delete_books'),
    
    # Library URLs
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('libraries/add/', views.add_library, name='add_library'),
    path('libraries/<int:pk>/edit/', views.edit_library, name='edit_library'),
    path('libraries/<int:pk>/delete/', views.delete_library, name='delete_library'),
    
    # Logout URL
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    # Login URL
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # Password change URLs
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='registration/password_change_form.html',
             success_url='/profile/'
         ), 
         name='password_change'),
    path('password-change/done/', 
         auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/password_change_done.html'
         ), 
         name='password_change_done'),
]

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Author, Book, Library, Librarian, UserProfile

# Unregister the default User admin
admin.site.unregister(User)

# Define an inline admin descriptor for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    
    def get_role(self, obj):
        return obj.userprofile.get_role_display()
    get_role.short_description = 'Role'

# Register the User admin
admin.site.register(User, UserAdmin)

# Register other models
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'book_count')
    search_fields = ('name',)
    
    def book_count(self, obj):
        return obj.book_set.count()
    book_count.short_description = 'Number of Books'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'published_date')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author__name')
    date_hierarchy = 'published_date'

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'book_count')
    search_fields = ('name',)
    filter_horizontal = ('books',)
    
    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Number of Books'

@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'library')
    search_fields = ('name', 'library__name')
    list_select_related = ('library',)

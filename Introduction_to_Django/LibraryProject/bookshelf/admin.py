from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Enable filtering by these fields
    list_filter = ('publication_year', 'author')
    
    # Enable search in these fields
    search_fields = ('title', 'author')
    
    # Order by title by default
    ordering = ('title',)

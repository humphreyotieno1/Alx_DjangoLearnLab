# Advanced API Project with Django REST Framework

This project demonstrates advanced API development with Django REST Framework, featuring custom serializers, views, and filtering capabilities.

## Features

- **CRUD Operations**: Full CRUD operations for Author and Book resources
- **Authentication**: Token-based authentication for protected endpoints
- **Filtering**: Filter books by author and publication year
- **Searching**: Full-text search across book titles and author names
- **Ordering**: Sort results by various fields
- **Pagination**: Results are paginated for better performance

## API Endpoints

### Books

- `GET /api/books/` - List all books with filtering, searching, and ordering
  - **Filters**:
    - `author`: Filter by author ID (exact match)
    - `publication_year`: Filter by year (exact, gt, lt, gte, lte)
    - Example: `/api/books/?author=1&publication_year__gt=2000`
  - **Search**:
    - `search`: Search in title and author name
    - Example: `/api/books/?search=harry`
  - **Ordering**:
    - `ordering`: Order by any field (prefix with - for descending)
    - Example: `/api/books/?ordering=-publication_year,title`

- `GET /api/books/<pk>/` - Retrieve a specific book
- `POST /api/books/` - Create a new book (authenticated only)
- `PUT /api/books/<pk>/` - Update a book (authenticated only)
- `PATCH /api/books/<pk>/` - Partially update a book (authenticated only)
- `DELETE /api/books/<pk>/` - Delete a book (authenticated only)

### Authors

- `GET /api/authors/` - List all authors
- `GET /api/authors/<pk>/` - Retrieve a specific author
- `POST /api/authors/` - Create a new author (authenticated only)
- `PUT /api/authors/<pk>/` - Update an author (authenticated only)
- `PATCH /api/authors/<pk>/` - Partially update an author (authenticated only)
- `DELETE /api/authors/<pk>/` - Delete an author (authenticated only)

## Setup and Installation

1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```

## Testing

To run tests:
```
python manage.py test api
```

## Authentication

Endpoints that modify data require authentication. You can authenticate using:

1. Session authentication (via the browsable API)
2. Basic authentication (for programmatic access)

## Dependencies

- Django
- Django REST Framework
- django-filter
- django-cors-headers

## License

This project is licensed under the MIT License - see the LICENSE file for details.

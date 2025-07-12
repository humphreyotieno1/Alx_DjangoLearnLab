# Creating a book

```python
from bookshelf.models import Book
Book.objects.create(title='1984', author='George Orwell', publication_year='1949')
```

```python
book = Book.objects.all()
```

```python
book
```

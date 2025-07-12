# Creating a book

```python
from bookshelf.models import Book
book1 = Book(title='1984', author='George Orwell', publication_year='1949')
book1.save()
```

```python
book = Book.objects.all()
```

```python
book1
```

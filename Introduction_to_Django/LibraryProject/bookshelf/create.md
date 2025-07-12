# Creating a book

```python
from bookshelf.models import Book
book1 = Book(title='Intro to Django', author='Humphrey Otieno', publication_year='2025')
book1.save()
```

```python
book = Book.objects.all()
```

```python
book1
```

# Deleting a book

```python
from bookshelf.models import Book
book = Book.objects.all()
```

```python
book
```

```python
book.title
```

```python
book.author
```

```python
book.publication_year
```

```python
book.delete()
```

```python
book = Book.objects.all()
```

```python
book
```

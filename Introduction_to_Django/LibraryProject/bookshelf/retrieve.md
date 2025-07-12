# Retrieving a book


```python
from bookshelf.models import Book
Book.objects.get(title='1984')
```

```python
book = Book.objects.get(title='1984')
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

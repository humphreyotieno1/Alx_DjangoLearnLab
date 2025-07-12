# CRUD Operations

## Create

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

```python
book.title
```

```python
book.author
```

```python
book.publication_year
```

## Retrieve

```python
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

## Update

```python
from bookshelf.models import Book
book = Book(title='Intro to Django', author='Humphrey Otieno', publication_year='2025')
book.save()
```

```python
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
book.title = 'Intro to Django 2'
book.save()
```

```python
book.title
```

## Delete

```python
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

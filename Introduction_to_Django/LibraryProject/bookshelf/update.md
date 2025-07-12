# Updating a book

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

```python
book.title = 'Intro to Django 2'
book.save()
```

```python
book.title
```

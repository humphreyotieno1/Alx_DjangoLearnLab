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
book.title = 'Nineteen Eighty-Four'
book.save()
```

```python
book.title
```

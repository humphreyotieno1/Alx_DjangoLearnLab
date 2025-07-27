from django import forms
from django.core.exceptions import ValidationError
from .models import Book

class ExampleForm(forms.Form):
    """
    An example form demonstrating form fields and validation.
    """
    name = forms.CharField(
        label='Your Name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        })
    )
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    message = forms.CharField(
        label='Your Message',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Type your message here...'
        })
    )
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise ValidationError("Name must be at least 3 characters long.")
        return name


class BookForm(forms.ModelForm):
    """
    Form for creating and updating Book instances.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'published_date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'published_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                },
                format='%Y-%m-%d'
            ),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
        }
    
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if not isbn.isdigit() or len(isbn) != 13:
            raise ValidationError("ISBN must be a 13-digit number.")
        return isbn
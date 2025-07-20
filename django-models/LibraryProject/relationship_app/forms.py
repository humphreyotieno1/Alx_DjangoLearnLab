from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Library, UserProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
            'publication_year': forms.NumberInput(attrs={ 
                'class': 'form-control',
                'min': 1000, 
                'max': 2100,
                'placeholder': 'e.g., 2023'
            }),
        }
        help_texts = {
            'publication_year': 'Enter a year between 1000 and 2100',
        }

    def clean_publication_year(self):
        publication_year = self.cleaned_data.get('publication_year')
        if publication_year < 1000 or publication_year > 2100:
            raise forms.ValidationError("Publication year must be between 1000 and 2100")
        return publication_year

class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['name', 'books']
        widgets = {
            'books': forms.CheckboxSelectMultiple(),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role']

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Book, Library, CustomUser

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Format: YYYY-MM-DD'
    )
    profile_photo = forms.ImageField(required=False)
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        initial='Member',
        help_text='Select user role'
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'email', 
            'date_of_birth', 'profile_photo', 'role',
            'password1', 'password2'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email unique
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control'})
        self.fields['profile_photo'].widget.attrs.update({'class': 'form-control'})
        self.fields['role'].widget.attrs.update({'class': 'form-select'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

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
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo', 'role']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields:
            if field == 'profile_photo':
                self.fields[field].widget.attrs.update({'class': 'form-control-file'})
            elif field == 'role':
                self.fields[field].widget.attrs.update({'class': 'form-select'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from taggit.forms import TagWidget
from .models import Post, Comment

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your post content here'}),
            'tags': TagWidget(attrs={'placeholder': 'Enter tags, separated by commas'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        return title

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Write your comment here', 'rows': 4}),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 5:
            raise forms.ValidationError('Comment must be at least 5 characters long.')
        return content
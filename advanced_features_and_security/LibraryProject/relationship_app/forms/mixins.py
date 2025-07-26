""
Form mixins for security enhancements.
"""
from django import forms
from django.core.exceptions import ValidationError
from ..utils.security import sanitize_input, validate_file_extension


class SecureFormMixin:
    """
    A mixin that adds security features to forms.
    - Automatic input sanitization
    - File upload validation
    - CSRF protection (built into Django)
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_security_attributes()
    
    def _add_security_attributes(self):
        """Add security-related HTML attributes to form fields."""
        for field_name, field in self.fields.items():
            # Add autocomplete attributes
            if field_name in ['username', 'email', 'password', 'new_password', 'current_password']:
                field.widget.attrs['autocomplete'] = 'off'
            
            # Add inputmode for better mobile keyboard support
            if isinstance(field, forms.EmailField):
                field.widget.attrs['inputmode'] = 'email'
            elif isinstance(field, (forms.URLField, forms.URLInput)):
                field.widget.attrs['inputmode'] = 'url'
            elif isinstance(field, (forms.NumberInput, forms.IntegerField, forms.DecimalField)):
                field.widget.attrs['inputmode'] = 'numeric'
            
            # Add spellcheck for text areas and inputs
            if isinstance(field.widget, forms.Textarea) or \
               (hasattr(field.widget, 'input_type') and field.widget.input_type in ['text', 'search']):
                field.widget.attrs['spellcheck'] = 'true'
    
    def clean(self):
        ""
        Clean and validate all form fields.
        Applies security sanitization to all fields.
        """
        cleaned_data = super().clean()
        
        for field_name, value in self.cleaned_data.items():
            if value is None or value == '':
                continue
                
            field = self.fields.get(field_name)
            
            # Skip file fields (handled separately)
            if hasattr(field, 'widget') and isinstance(field.widget, forms.FileInput):
                continue
                
            # Determine field type for sanitization
            field_type = self._get_field_type(field)
            
            try:
                cleaned_value = sanitize_input(value, field_type=field_type)
                self.cleaned_data[field_name] = cleaned_value
            except ValidationError as e:
                self.add_error(field_name, e)
        
        return cleaned_data
    
    def _get_field_type(self, field):
        """Determine the field type for sanitization."""
        if isinstance(field, forms.EmailField):
            return 'email'
        elif isinstance(field, forms.URLField):
            return 'url'
        elif isinstance(field, (forms.IntegerField, forms.DecimalField, forms.FloatField)):
            return 'number'
        elif isinstance(field, forms.DateField):
            return 'date'
        return 'text'
    
    def clean_file_field(self, field_name, allowed_extensions=None, max_size=5*1024*1024):
        """
        Clean and validate a file upload field.
        
        Args:
            field_name: Name of the file field
            allowed_extensions: List of allowed file extensions (default: common image types)
            max_size: Maximum file size in bytes (default: 5MB)
            
        Returns:
            The cleaned file or None if no file was uploaded
            
        Raises:
            ValidationError: If the file is invalid
        """
        file_field = self.cleaned_data.get(field_name)
        
        if not file_field:
            return None
            
        # Check file size
        if hasattr(file_field, 'size') and file_field.size > max_size:
            raise ValidationError(f'File too large. Maximum size is {max_size//1024//1024}MB.')
            
        # Check file extension
        validate_file_extension(file_field, allowed_extensions)
        
        # Sanitize filename
        if hasattr(file_field, 'name'):
            file_field.name = sanitize_filename(file_field.name)
            
        return file_field


class SecureModelFormMixin(SecureFormMixin):
    ""
    Secure form mixin for ModelForms.
    Adds model instance tracking for security.
    """
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        """Save the model instance with additional security checks."""
        instance = super().save(commit=False)
        
        # Track the user who created or modified the instance
        if hasattr(instance, 'created_by') and not instance.pk:
            if self.request and hasattr(self.request, 'user') and self.request.user.is_authenticated:
                instance.created_by = self.request.user
                
        if hasattr(instance, 'last_modified_by') and self.request and hasattr(self.request, 'user'):
            if self.request.user.is_authenticated:
                instance.last_modified_by = self.request.user
        
        if commit:
            instance.save()
            self.save_m2m()
            
        return instance

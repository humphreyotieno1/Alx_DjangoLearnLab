""
Security utilities for input validation and sanitization.
"""
import re
from html import escape
from urllib.parse import urlparse
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.utils.text import slugify


def sanitize_input(input_data, field_type='text'):
    """
    Sanitize and validate user input based on field type.
    
    Args:
        input_data: The input data to sanitize
        field_type: The type of field ('text', 'email', 'url', 'number', 'date')
        
    Returns:
        Sanitized input data
        
    Raises:
        ValidationError: If input is invalid for the specified field type
    """
    if input_data is None:
        return None
        
    # Convert to string and strip whitespace
    if not isinstance(input_data, str):
        input_data = str(input_data)
    
    input_data = input_data.strip()
    
    # Field type specific validation and sanitization
    if field_type == 'email':
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', input_data):
            raise ValidationError('Invalid email format')
        return input_data.lower()
        
    elif field_type == 'url':
        try:
            result = urlparse(input_data)
            if not all([result.scheme, result.netloc]):
                raise ValidationError('Invalid URL format')
            return input_data
        except Exception:
            raise ValidationError('Invalid URL format')
            
    elif field_type == 'number':
        if not input_data.isdigit():
            raise ValidationError('Must be a number')
        return input_data
        
    elif field_type == 'date':
        # Basic date format validation (YYYY-MM-DD)
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', input_data):
            raise ValidationError('Date must be in YYYY-MM-DD format')
        return input_data
        
    # Default text sanitization
    return escape(strip_tags(input_data))


def validate_file_extension(file, allowed_extensions=None):
    """
    Validate file extension against a whitelist.
    
    Args:
        file: The file object to validate
        allowed_extensions: List of allowed file extensions (e.g., ['jpg', 'png', 'pdf'])
        
    Raises:
        ValidationError: If file extension is not allowed
    """
    if allowed_extensions is None:
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'pdf']
        
    ext = file.name.split('.')[-1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(
            f'File type not allowed. Allowed types: { ", ".join(allowed_extensions) }'
        )


def sanitize_filename(filename):
    """
    Sanitize a filename by removing or replacing potentially dangerous characters.
    """
    # Remove directory traversal attempts
    filename = os.path.basename(filename)
    # Replace whitespace and special characters with underscores
    filename = re.sub(r'[\s\/\\\?%\*:|"<>\x00-\x1f\x7f]', '_', filename)
    # Remove multiple consecutive underscores
    filename = re.sub(r'_+', '_', filename).strip('_')
    return filename


def safe_redirect_url(url, allowed_domains=None, default='/'):
    """
    Validate a redirect URL to prevent open redirect vulnerabilities.
    
    Args:
        url: The URL to validate
        allowed_domains: List of allowed domains (defaults to current site domain)
        default: Default URL if validation fails
        
    Returns:
        A safe redirect URL
    """
    if not url:
        return default
        
    # If it's a relative URL, it's safe
    if url.startswith('/'):
        return url
        
    # Parse the URL and check if domain is allowed
    try:
        parsed = urlparse(url)
        if not parsed.netloc:  # No domain, relative URL
            return url
            
        # Check against allowed domains
        if allowed_domains is None:
            from django.contrib.sites.shortcuts import get_current_site
            current_site = get_current_site(None)
            allowed_domains = [current_site.domain]
            
        if parsed.netloc not in allowed_domains:
            return default
            
        return url
    except Exception:
        return default

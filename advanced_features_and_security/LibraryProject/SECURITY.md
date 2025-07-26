# Security Implementation Guide

This document outlines the security measures implemented in the Library Management System to protect against common web vulnerabilities.

## Table of Contents
1. [Security Headers](#security-headers)
2. [HTTPS and Secure Cookies](#https-and-secure-cookies)
3. [Content Security Policy (CSP)](#content-security-policy)
4. [Input Validation and Sanitization](#input-validation-and-sanitization)
5. [Cross-Site Request Forgery (CSRF) Protection](#cross-site-request-forgery-csrf-protection)
6. [Cross-Site Scripting (XSS) Protection](#cross-site-scripting-xss-protection)
7. [Secure File Uploads](#secure-file-uploads)
8. [Django Security Middleware](#django-security-middleware)
9. [Security Testing](#security-testing)
10. [Deployment Security](#deployment-security)

## Security Headers

The application includes the following security headers:

- **X-Content-Type-Options: nosniff** - Prevents MIME type sniffing
- **X-Frame-Options: DENY** - Prevents clickjacking attacks
- **X-XSS-Protection: 1; mode=block** - Enables XSS filtering in browsers
- **Content-Security-Policy** - Restricts resources that can be loaded (see CSP section)
- **Referrer-Policy: strict-origin-when-cross-origin** - Controls referrer information
- **Permissions-Policy** - Restricts browser features usage

## HTTPS and Secure Cookies

- **SECURE_SSL_REDIRECT = True** - Redirects all non-HTTPS requests to HTTPS
- **SESSION_COOKIE_SECURE = True** - Ensures session cookies are only sent over HTTPS
- **CSRF_COOKIE_SECURE = True** - Ensures CSRF cookies are only sent over HTTPS
- **SESSION_COOKIE_HTTPONLY = True** - Prevents JavaScript access to session cookies
- **CSRF_COOKIE_HTTPONLY = True** - Additional protection for CSRF cookies

## HTTP Strict Transport Security (HSTS)

- **SECURE_HSTS_SECONDS = 31536000** - Enables HSTS for 1 year
- **SECURE_HSTS_INCLUDE_SUBDOMAINS = True** - Applies to all subdomains
- **SECURE_HSTS_PRELOAD = True** - Allows preloading in browsers

## Content Security Policy (CSP)

The application implements a strict CSP that:

- Only allows loading resources (scripts, styles, images, etc.) from trusted sources
- Prevents inline JavaScript execution (except for nonces in development)
- Restricts form submissions to same-origin by default
- Prevents framing of the application

## Input Validation and Sanitization

### Server-Side Validation

All form inputs are validated and sanitized using the `SecureFormMixin` which provides:

- Automatic input sanitization based on field type
- Protection against XSS attacks
- Consistent validation rules across all forms
- Secure handling of file uploads

### Secure Form Fields

- Email fields are validated for proper format
- URLs are validated to prevent open redirects
- File uploads are restricted by extension and size
- All text inputs are sanitized to prevent XSS

## Cross-Site Request Forgery (CSRF) Protection

- CSRF protection is enabled by default in Django
- All forms include the `{% csrf_token %}` template tag
- CSRF tokens are only sent over HTTPS
- CSRF cookie is HTTPOnly for additional protection

## Cross-Site Scripting (XSS) Protection

- Automatic escaping of variables in templates
- Marked template variables as `|safe` only when necessary
- Content Security Policy to prevent inline JavaScript execution
- Input sanitization for all user-provided content

## Secure File Uploads

File uploads are secured by:

1. Validating file extensions against a whitelist
2. Limiting maximum file size
3. Sanitizing filenames to prevent directory traversal
4. Storing files outside the web root when possible
5. Using unique filenames to prevent overwriting

## Django Security Middleware

The application includes a custom `SecurityHeadersMiddleware` that adds security headers to all responses and implements the Content Security Policy.

## Security Testing

### Automated Testing

Run the security tests with:

```bash
python manage.py test relationship_app.tests.test_security
```

### Manual Testing

1. **CSRF Protection**
   - Try submitting forms without a valid CSRF token
   - Verify that the form submission is rejected

2. **XSS Protection**
   - Try entering script tags in input fields
   - Verify that the scripts are properly escaped

3. **Authentication**
   - Test login/logout functionality
   - Verify that protected pages require authentication

4. **Authorization**
   - Test that users can only access authorized resources
   - Verify that permission checks are working correctly

## Deployment Security

### Required Settings for Production

1. **Secret Key**
   - Generate a new secret key for production
   - Store it in an environment variable, not in version control

2. **Database**
   - Use a production-ready database (PostgreSQL recommended)
   - Ensure the database user has the minimum required permissions

3. **Static and Media Files**
   - Configure a separate web server (Nginx/Apache) to serve static files
   - Store media files outside the project directory

4. **HTTPS**
   - Obtain an SSL certificate from a trusted CA
   - Configure your web server to redirect all HTTP traffic to HTTPS

### Security Headers Check

After deployment, verify your security headers using:

- [Security Headers](https://securityheaders.com/)
- [Mozilla Observatory](https://observatory.mozilla.org/)

## Reporting Security Issues

If you discover a security vulnerability, please report it to the project maintainers at [security@example.com].

## Additional Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)

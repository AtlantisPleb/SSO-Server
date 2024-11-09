import os
from .settings import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ['.herokuapp.com', 'oidc1-052bc9374cf6.herokuapp.com']

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# Static files configuration
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Ensure we're using PostgreSQL
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'

# Add your Heroku app domain to CORS and CSRF settings
CORS_ALLOWED_ORIGINS = [
    'https://oidc1-052bc9374cf6.herokuapp.com',
] + CORS_ALLOWED_ORIGINS

CSRF_TRUSTED_ORIGINS = [
    'https://oidc1-052bc9374cf6.herokuapp.com',
] + CSRF_TRUSTED_ORIGINS
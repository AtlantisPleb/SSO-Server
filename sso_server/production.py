import os
from .settings import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ['.herokuapp.com']

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

__author__ = 'kako'

# Import defaults

from .base import *


# Debug level

DEBUG = False
TASTYPIE_FULL_DEBUG = False


# Request listener

ALLOWED_HOSTS = ['*']


# CORS allowed domains

CORS_ORIGIN_WHITELIST = (
    'forecast.escng.com',
)


# Database configuration

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', 5432),
        'NAME': os.environ.get('DB_NAME', 'pjtracker'),
        'USER': os.environ.get('DB_USER', 'pjtracker'),
        'PASSWORD': os.environ.get('DB_PASS', 'pjtracker'),
    }
}


# Database bootstrapping options

BOOTSTRAP_EXAMPLE_ACCOUNT = False
BOOTSTRAP_EXAMPLE_DATA = False


# Static media

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Logging handlers

LOGGING['handlers'] = {
    'file': {
        'class': 'logging.FileHandler',
        'formatter': 'verbose',
        'filename': '/var/log/django/pjtracker.log',
    }
}

LOGGING['loggers']['django']['handlers'] = ['file']

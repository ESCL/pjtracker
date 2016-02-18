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
        'HOST': 'pjtracker0.c8hyiihqnbry.us-east-1.rds.amazonaws.com',
        'PORT': 5432,
        'NAME': 'pjtracker',
        'USER': 'pjtracker',
        'PASSWORD': 'tr4ckmypjs',
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

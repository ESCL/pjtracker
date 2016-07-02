__author__ = 'kako'

# Import defaults

from .base import *


# Debug level

DEBUG = True
TASTYPIE_FULL_DEBUG = True


# CORS allowed domains

CORS_ORIGIN_ALLOW_ALL = True


# Set nose as test runner

INSTALLED_APPS.append('django_nose')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--verbosity=2']


# Database bootstrapping

BOOTSTRAP_EXAMPLE_ACCOUNT = True


# Logging handlers

LOGGING['handlers'] = {
    'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'verbose'
    }
}

LOGGING['loggers']['django']['handlers'] = ['console']

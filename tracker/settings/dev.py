__author__ = 'kako'

# Import defaults

from .base import *


# Extra apps for

INSTALLED_APPS.extend([
    # Better test runner (for coverage reports)
    'django_nose'
])


# Debug level

DEBUG = True
TASTYPIE_FULL_DEBUG = True


# CORS allowed domains

CORS_ORIGIN_ALLOW_ALL = True


# Database bootstrapping

BOOTSTRAP_EXAMPLE_ACCOUNT = True
BOOTSTRAP_EXAMPLE_DATA = True


# Logging handlers

LOGGING['handlers'] = {
    'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'verbose'
    }
}

LOGGING['loggers']['django']['handlers'] = ['console']


# Test options

#TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

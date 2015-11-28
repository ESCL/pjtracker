__author__ = 'kako'

from .base import *


DEBUG = False

ALLOWED_HOSTS = ['*']


DATABASES['default'].update({
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'HOST': 'pjtracker0.c8hyiihqnbry.us-east-1.rds.amazonaws.com',
    'PORT': 5432,
    'NAME': 'pjtracker',
    'USER': 'pjtracker',
    'PASSWORD': 'tr4ckmypjs'
})


STATIC_ROOT = os.path.join(BASE_DIR, 'static')

BOOTSTRAP_EXAMPLE_ACCOUNT = False
BOOTSTRAP_EXAMPLE_DATA = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/var/log/django/pjtracker.log',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
    },
}

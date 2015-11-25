__author__ = 'kako'

from .base import *


DEBUG = False

ALLOWED_HOSTS = ['*']


DATABASES['default'].update({
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'HOST': 'localhost',
    'PORT': 5432,
    'NAME': 'pjtracker',
    'USER': 'pjtracker',
    'PASSWORD': 'pjtracker'
})


STATIC_ROOT = os.path.join(BASE_DIR, 'static')

BOOTSTRAP_EXAMPLE_ACCOUNT = False
BOOTSTRAP_EXAMPLE_DATA = False

__author__ = 'kako'

from .base import *


DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

BOOTSTRAP_EXAMPLE_ACCOUNT = True
BOOTSTRAP_EXAMPLE_DATA = False
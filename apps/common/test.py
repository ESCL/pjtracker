__author__ = 'kako'

# Import abstraction for PyPy vs CPython

try:
    import mock
except ImportError:
    from unittest import mock

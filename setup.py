"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
__author__ = 'kako'

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pjtracker',

    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.2.0',

    description='Project resources tracker',
    long_description=long_description,
    url='https://github.com/ESCL/pjtracker',
    author='Claudio Omar Melendrez Baeza',
    author_email='claudio.melendrez@escng.com',
    license='http://pjtracker.com/terms',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Customer Service',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Office/Business',
    ],

    keywords='pjtracker project control resource tracking',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],
    extras_require={},
    package_data={},

    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={},
)

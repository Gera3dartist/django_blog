import os
import sys
import logging
from .settings import INSTALLED_APPS, MIDDLEWARE_CLASSES

__author__ = 'agerasym'


DEBUG = True
USE_HANDLER = True
INTERNAL_IPS = (
    '127.0.0.1'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'blog_db',
        'USER': 'postgres',
        'PASSWORD': '1111',
        'HOST': '127.0.0.1',
        'PORT': 5432,
        'TEST_NAME': 'test_blog_db',
        'TEST_MIRROR': 'default'
    }
}

TEST_RUNNER = 'django_blog.TestImportCustom'

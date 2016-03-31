from .base import *  # noqa
import os


DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'craigomatic',
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

from .base import *  # noqa
import os

import dj_database_url

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')

# Update database configuration with ${DATABASE_URL}.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

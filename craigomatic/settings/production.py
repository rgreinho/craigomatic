from .base import *  # noqa
import os

import dj_database_url

# Disable debug modes.
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# Get tbe production secret from the environment variables.
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# Get tbe production allowed hosts from the environment variables, or limit it to localhost only.
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')

# Update database configuration with ${DATABASE_URL}.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

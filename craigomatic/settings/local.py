from .base import *  # noqa


ADMINS = (
    ('Rémy Greinhofer', 'remy.greinhofer@gmail.com'),
) # yapf: disable

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'craigomatic',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# You might want to use sqlite3 for testing in local as it's much faster.
if IN_TESTING:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': '/tmp/craigomatic_test.db', }}

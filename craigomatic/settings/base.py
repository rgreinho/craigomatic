import os
from urllib.parse import urlparse
import sys

import dj_database_url

# PATH vars
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def root(x):
    return os.path.join(BASE_DIR, x)

# Insert the apps dir at the top of your path.
sys.path.insert(0, root('apps'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'CHANGE THIS!!!'

# SECURITY WARNING: don't run with debug turned on in production!
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# Allow all host headers
# SECURITY WARNING: don't run with this setting in production!
ALLOWED_HOSTS = ['*']

# Django applications.
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
]  # yapf: disable

# 3rd party apps.
THIRD_PARTY_APPS = [
    'djcelery',
    'kombu.transport.django',
]  # yapf: disable

# Project applications.
PROJECT_APPS = [
    'craigmine',
]  # yapf: disable

# Installed apps is a combination of all the apps.
# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE_CLASSES = [
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = 'craigomatic.urls'

# Define the site admins.
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Rémy Greinhofer', 'remy.greinhofer@gmail.com'),
)  # yapf: disable

# Define site managers.
# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# Python dotted path to the WSGI application used by Django's runserver.
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'craigomatic.wsgi.application'

# Internationalization.
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = root('static')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# Additional locations of static files.
# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    root('assets'),
)  # yapf: disable

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Templates configuration.
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            root('templates'),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]  # yapf: disable

# Password validation.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Database configuration.
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}  # yapf: disable

# Update database configuration with ${DATABASE_URL}.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Cache configuration.
redis_url = urlparse(os.environ.get('REDIS_URL', 'redis://redis:6379'))
CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "{0}:{1}".format(redis_url.hostname, redis_url.port),
        "OPTIONS": {
            "PASSWORD": redis_url.password,
            "DB": 0,
        }
    }
}

# Celery configuration.
BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'django://')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'djcelery.backends.database:DatabaseBackend')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

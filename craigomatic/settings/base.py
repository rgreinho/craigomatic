import os
from urllib.parse import urlparse
import sys

import dj_database_url

# PATH vars
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def root(x):
    return os.path.join(BASE_DIR, x)


sys.path.insert(0, root('apps'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'CHANGE THIS!!!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow all host headers
# SECURITY WARNING: don't run with this setting in production!
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]  # yapf: disable

PROJECT_APPS = [
    'craigmine',
    'django_crontab',
]  # yapf: disable

INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'craigomatic.urls'

ADMINS = (
    ('Rémy Greinhofer', 'remy.greinhofer@gmail.com'),
)  # yapf: disable

MANAGERS = ADMINS

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'craigomatic.wsgi.application'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = root('static')
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    root('assets'),
)  # yapf: disable

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Templates
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

# Password validation
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

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}  # yapf: disable

# Update database configuration with ${DATABASE_URL}.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Cache
redis_url = urlparse(os.environ.get('REDIS_URL'))
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "{0}:{1}".format(redis_url.hostname, redis_url.port),
        "OPTIONS": {
            "PASSWORD": redis_url.password,
            "DB": 0,
        }
    }
}

# Django-crontab
CRONJOBS = [
    ('* 4,10,16,22 * * *', 'craigmine.management.commands.index.index_content'),
    ('* 2 * * *', 'craigmine.management.commands.purge.delete_items', ['7']),
]

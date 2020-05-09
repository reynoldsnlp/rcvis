"""
Django settings for rcvis project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['RCVIS_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['RCVIS_DEBUG'] == "True"

# I'm not proud of this. Add hosts - one per environment variable
ALLOWED_HOSTS = [os.environ['RCVIS_HOST']]
if 'RCVIS_HOST_ALIAS' in os.environ:
    ALLOWED_HOSTS.append(os.environ['RCVIS_HOST_ALIAS'])
if 'RCVIS_HOST_ALIAS_2' in os.environ:
    ALLOWED_HOSTS.append(os.environ['RCVIS_HOST_ALIAS_2'])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'visualizer',
    'bakery',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rcvis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rcvis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

# Options for the bakery
BUILD_DIR = os.path.join(BASE_DIR, os.environ['BAKED_DIRECTORY'])
BAKERY_VIEWS = (
    'visualizer.views.Index',
    'visualizer.views.Visualize',
    'visualizer.views.VisualizeEmbedded',
    'visualizer.views.Oembed'
)
STATIC_ROOT = os.path.join(BASE_DIR, os.environ['STATIC_ROOT'])
AWS_REGION = 'us-west-1'
AWS_BUCKET_NAME = 'rcvis-bakery'

# Uploaded media
OFFLINE_MODE = os.environ['OFFLINE_MODE'] == "True"
if not OFFLINE_MODE:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME=os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_S3_REGION_NAME=os.environ['AWS_S3_REGION_NAME']
    AWS_ACCESS_KEY_ID=os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY']
AWS_DEFAULT_ACL = None

# CELERY STUFF
CELERY_BROKER_URL = "sqs://"
CELERY_DEFAULT_QUEUE = "rcvis-queue"
#BROKER_URL = 'django://'

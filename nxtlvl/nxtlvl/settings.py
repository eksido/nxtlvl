"""
Django settings for nxtlvl project.

Generated by 'django-admin startproject' using Django 1.9.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import dj_database_url as dburl


def environ(key):
    """
    returns True if the key exists in os.environ[] and it is not false'ish
    """

    if not key in os.environ.keys():
        return False
    if os.environ[key] and os.environ[key] != '0':
        return True

    return False


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8ss(&x)91zoj38!$1un&b!p)%kurykbp1*uq^@rv5(jj=2!=so'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

PROJECT_DIR = os.path.dirname(__file__)

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.sites',
    'ensomus',
    'tinymce',
    'bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'nxtlvl.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'nxtlvl.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
#
# MYSQL steps to create database and user:
#
# CREATE DATABASE nxtlvl_db CHARACTER SET utf8 COLLATE utf8_general_ci;
# CREATE USER 'nxtlvl_user' IDENTIFIED BY '1q2w3e4r';
# GRANT ALL ON nxtlvl_db.* TO 'nxtlvl_user'@'localhost' IDENTIFIED BY '1q2w3e4r';
# GRANT ALL ON nxtlvl_db.* TO 'nxtlvl_user'@'%' IDENTIFIED BY '1q2w3e4r';
# FLUSH PRIVILEGES;
#
# Define DATABASE_URL in your local environment by running:
#
# export DATABASE_URL="mysql://nxtlvl_user:1q2w3e4r@localhost:3306/nxtlvl_db"
#
DATABASES = {
    'reference': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nxtlvl_test',
        'USER': 'nxtlvl_user',
        'PASSWORD': '1q2w3e4r',

    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }

}

# Overwriting `default` from environment's DATABASE_URL
if environ('DATABASE_URL'):
    DATABASES['default'] = dburl.config()
else:
    raise Exception('Database settings not found. Please add DATABASE_URL to your environment')

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

# TinyMCE

TINYMCE_COMPRESSOR = False

TINYMCE_DEFAULT_CONFIG = {

    'theme': "advanced",

}

TINYMCE_JS_URL = '/static/js/tiny_mce/tiny_mce.js'

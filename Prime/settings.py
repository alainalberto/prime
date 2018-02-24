"""
Django settings for Prime project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import socket

from django.core.urlresolvers import reverse_lazy
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o*&&#z_i@5cmck_-xh8n84wywwp%bmypco2^-#3(^z((69z)2v'

# SECURITY WARNING: don't run with debug turned on in production!
if socket.gethostname() == 'Ransel-PC' or socket.gethostname() == 'alain-HP-Notebook':
    DEBUG = True
    ALLOWED_HOSTS = []
else:
    DEBUG = False
    ALLOWED_HOSTS = ['159.65.250.237', 'www.prime1agency.com','prime1agency.com', 'http://prime1agency.com/']


# Application definition

INSTALLED_APPS = [
    #DJango Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.sites',
   # 'django.contrib.flatpages',
    'django.contrib.humanize',

    #My Apps
    'apps.tools',
    'apps.accounting',
    'apps.logistic',
    'apps.services',

    #External
    'django_tables2',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

AUTO_LOGOUT_DELAY = 15

SESSION_IDLE_TIMEOUT = 60

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 300 # set just 5 min to test
SESSION_SAVE_EVERY_REQUEST = True

ROOT_URLCONF = 'Prime.urls'

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

if not DEBUG:
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    STATIC_ROOT = '/root/prime/static_pro'
    MEDIA_ROOT =  '/root/prime/static/media'

    STATICFILES_DIRS = (
        '/home/root/prime/static',
    )
else:

    STATIC_URL = '/static/'

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
        # '/var/www/static',
    ]

    STATIC_ROOT = os.path.join(BASE_DIR, 'static_pro')

    MEDIA_URL = '/media/'

    MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')

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
                'Prime.context_processors.base',
            ],
        },
    },
    ]

WSGI_APPLICATION = 'Prime.wsgi.application'

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
if socket.gethostname() == 'Ransel-PC' or socket.gethostname() == 'alain-HP-Notebook':
   DATABASES = {
      'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'db_muestra',
         'USER': 'administrator',
         'PASSWORD': 'admin*2017',
         'HOST': 'localhost',
         'PORT': '5432',
          }
      }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'aacub_prime_db',
            'USER': 'aacub_administrator',
            'PASSWORD': 'admin*2017',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_REDIRECT_URL = reverse_lazy('login')





ADMINS = (
('Alain Alberto', 'alainalberto03@gmail.com'),
('Ransel Ramos ', 'ranselr@gmail.com'),
)

MANAGERS = (
('Alain Alberto', 'alainalberto03@gmail.com'),
('Ransel Ramos ', 'ranselr@gmail.com'),
)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ins@firstcallintermodal.com'
EMAIL_HOST_PASSWORD = 'Morton160'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_SUBJECT_PREFIX = 'ERROR-PRIME'

CRISPY_TEMPLATE_PACK = 'bootstrap3'


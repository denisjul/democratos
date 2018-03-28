"""
Django settings for democratos project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
from __future__ import absolute_import

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c-#yroc+js)qb2h899%oax*lu473m8!c7bt35)md_^7*9$3kna'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'CreateYourLaws',
    'captcha',
    'registration',
    'ckeditor',
    #'werkzeug',
    'render_block',
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

ROOT_URLCONF = 'democratos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), PROJECT_PATH],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG
        },
    },
]

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'xapian_backend.XapianEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'xapian_index')
    },
}

WSGI_APPLICATION = 'democratos.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'democratos_db',
        'USER': 'superjuju',
        'PASSWORD': 'UWBddw75',
        'HOST': 'localhost',
        'PORT': '',
    }
}
"""



SESSION_EXPIRE_AT_BROWSER_CLOSE = True

AUTH_USER_MODEL = 'CreateYourLaws.CYL_user'

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

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/


# Settings for django-registration-redux
SITE_ID = 1
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
LOGIN_REDIRECT_URL = '/CYL/'  # after successful log in
LOGIN_URL = '/CYL/accounts/login/'  # directed to if they are not logged in,
REGISTRATION_FORM = 'CreateYourLaws.forms.Create_CYL_UserForm'
# LOGOUT_REDIRECT_URL = '/CYL/accounts/login/'
# and are trying to access pages requiring authentication

# Settings for ckeditors

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")
STATIC_ROOT = os.path.join(PROJECT_PATH, "static")


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['Cut', 'Copy', 'Paste', '-', 'Undo', 'Redo'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-',
             'Blockquote', 'SpecialChar', 'Smiley', '-',
             'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            # 'Language'],
            ['About'],
            '/',
            ['tableinsert', 'tabledelete', 'tableproperties', '-',
             'tablerowinsertbefore', 'tablerowinsertafter', 'tablerowdelete',
             '-', 'tablecolumninsertbefore', 'tablecolumninsertafter',
             'tablecolumndelete', '-', 'tablecellinsertbefore',
             'tablecellinsertafter', 'tablecelldelete', 'tablecelldelete', '-',
             'tablecellsmerge', 'tablecellsplithorizontal',
             'tablecellsplitvertical'],
        ],
        'extraPlugins': ','.join(
            [
                'div',
                'autolink',
                'tabletoolstoolbar',
                'autogrow',
                'wordcount',
                'notification',
                'widget',
                'lineutils',
                'clipboard',
                'elementspath',
                'ajax',
                'embed',
                'codesnippet',
            ]),
        'width': '100%',
    },

    'redac_law': {
        'toolbar': 'redac_law',
        'toolbar_redac_law': [
            ['Bold', 'Italic', 'Underline'],
            ['Cut', 'Copy', 'Paste', '-', 'Undo', 'Redo'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-',
             'Blockquote', 'SpecialChar', '-',
             'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            # 'Language'],
            ['About'],
            '/',
            ['tableinsert', 'tabledelete', 'tableproperties', '-',
             'tablerowinsertbefore', 'tablerowinsertafter', 'tablerowdelete',
             '-', 'tablecolumninsertbefore', 'tablecolumninsertafter',
             'tablecolumndelete', '-', 'tablecellinsertbefore',
             'tablecellinsertafter', 'tablecelldelete', 'tablecelldelete', '-',
             'tablecellsmerge', 'tablecellsplithorizontal',
             'tablecellsplitvertical'],
        ],
        'width': '100%',
        'extraPlugins': ','.join(
            [
                'div',
                'autolink',
                'tabletoolstoolbar',
                'autogrow',
                'wordcount',
                'notification',
                'widget',
                'lineutils',
                'clipboard',
                'elementspath',
                'ajax',
                'embed',
                'codesnippet',
            ]),
    }
}
"""
CKEDITOR_UPLOAD_PATH = "uploads/"
"""
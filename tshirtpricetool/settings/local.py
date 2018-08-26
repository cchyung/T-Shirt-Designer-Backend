from tshirtpricetool.settings.base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': 'tshirtdesigner',
        'USER': 'admin',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
        'ENGINE': 'django.db.backends.postgresql_psycopg2'
    }
}
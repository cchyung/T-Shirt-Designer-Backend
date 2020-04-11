from tshirtpricetool.settings.base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'NAME': 'tshirtdesigner',
#         'USER': 'admin',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '',
#         'ENGINE': 'django.db.backends.postgresql_psycopg2'
#     }
# }

DATABASES = {
    'default': {
        'NAME': 'd23amtt7hdlrgt',
        'USER': 'pwezlcfidhdgui',
        'PASSWORD': '68268732ca70c8ac35c0e76bf57f2e05c928ee6baa02114e6fb867cf7d42eab3',
        'HOST': 'ec2-54-243-216-33.compute-1.amazonaws.com',
        'PORT': '5432',
        'ENGINE': 'django.db.backends.postgresql_psycopg2'
    }
}



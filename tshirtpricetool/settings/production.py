from tshirtpricetool.settings.base import *
import dj_database_url

DEBUG = False

db_from_env = dj_database_url.config(conn_max_age=500)

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': db_from_env
}
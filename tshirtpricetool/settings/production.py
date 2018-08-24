from tshirtpricetool.settings.base import *
import dj_database_url
import django_heroku

DEBUG = True


db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

django_heroku.settings(locals())
import os
import sys
import urlparse
import socket

urlparse.uses_netloc.append('postgres')
urlparse.uses_netloc.append('mysql')
urlparse.uses_netloc.append('sqlite')

env = lambda key, returntype=str: returntype(os.environ[key])

DEBUG = env('DJANGO_DEBUG', bool)
TEMPLATE_DEBUG = DEBUG

MIDDLEWARE_CLASSES = (
    'supstream.middleware.VHostMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'gunicorn',
    'djapp',
    'supstream',
)

# HEROKU_NO_DJANGO_SETTINGS
DATABASES = dict(default={})
def parse_database_url(database, environment_variable='DATABASE_URL'):
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    database.update({
        'NAME': url.path[1:],
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port,
        'ENGINE' : {
            'postgres': 'django.db.backends.postgresql_psycopg2',
            'mysql': 'django.db.backends.mysql',
            'sqlite': 'django.db.backends.sqlite3',
        }[url.scheme],
    })
parse_database_url(DATABASES['default'])
del parse_database_url

DOMAIN = env('DOMAIN')
if os.environ['NETLOC_SUFFIX']:
    NETLOC_SUFFIX = env('NETLOC_SUFFIX')
else:
    NETLOC_SUFFIX = '%s.%s:%s' % (socket.gethostname().split('.')[0], DOMAIN, os.environ['PORT'])
HOST_SUFFIX = NETLOC_SUFFIX.split(':')[0]

STATIC_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
STATIC_URL = '//static.' + NETLOC_SUFFIX

MEDIA_ROOT = ''
MEDIA_URL = ''

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

ADMINS = ()
MANAGERS = ADMINS
SITE_ID = 1
SECRET_KEY = env('DJANGO_SECRET_KEY')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
)

ROOT_URLCONF = 'djproj.urls.root'
VHOST_URLCONFS = dict(
    static = 'djproj.urls.static',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'SLUG_UUID')) as handle:
        RELEASE_ID=handle.read().strip()
except IOError:
    pass


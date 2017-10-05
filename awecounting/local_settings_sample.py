from settings import *

SECRET_KEY = '=s0$)ng6s4x@tt=e+v3hygikjuwn3d_m1ihz$m07e(g#bhj)pp'

ADMINS = [('Dipesh Acharya', 'xtranophilist@gmail.com')]
SERVER_EMAIL = 'webmaster@xawecounting.com'

DEBUG = True
MODELTRANSLATION_DEBUG = DEBUG

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = '/media/'

INSTALLED_APPS += (
    # 'debug_toolbar',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dbname',
        'USER': 'awecounting',
        'PASSWORD': '',
        'HOST': 'db',
        'PORT': '',
    }
}

ALLOWED_HOSTS = ['beta.awecounting.com', 'awecounting.com', 'www.awecounting.com', 'localhost', '127.0.0.1']

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, '..', 'emails')

import sys

if 'test' in sys.argv or 'test_coverage' in sys.argv:  # Covers regular testing and django-coverage
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
    DEBUG = False
    TEMPLATE_DEBUG = False
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

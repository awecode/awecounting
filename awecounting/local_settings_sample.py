from settings import *

SECRET_KEY = '=s0$)ng6s4x@tt=e+v3hygikjuwn3d_m1ihz$m07e(g#bhj)pp'

ADMINS = [('Dipesh Acharya', 'xxtranophilist@gmail.com')]
SERVER_EMAIL = 'webmaster@xawecounting.com'

DEBUG = True
MODELTRANSLATION_DEBUG = DEBUG

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = '/media/'

INSTALLED_APPS += (
    'debug_toolbar',
)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'awecounting',
#         'USER': 'awecounting',
#         'PASSWORD': 'password',
#         'HOST': '',
#         'PORT': '',
#         'ATOMIC_REQUESTS': True,
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

ALLOWED_HOSTS = []

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

gettext = lambda s: s

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


INSTALLED_APPS = (
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # apps
    'inventory',
    'ledger',

    'rest_framework',
    'linaro_django_pagination',
    'webstack_django_sorting',
    'reversion',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'linaro_django_pagination.middleware.PaginationMiddleware',
    'webstack_django_sorting.middleware.SortingMiddleware',
)

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'app.wsgi.application'

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', gettext('English')),
    ('ne', gettext("Nepali")),
]

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_L10N = True

USE_TZ = True

try:
    from .local_settings import *  # noqa
except ImportError:
    pass

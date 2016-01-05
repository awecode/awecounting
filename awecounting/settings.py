import os
from django.contrib import messages

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

gettext = lambda s: s

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

INSTALLED_APPS = (
    'apps.users',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.inventory',
    'apps.ledger',
    'apps.share',
    'apps.bank',
    'apps.voucher',

    'njango',
    'rest_framework',
    'linaro_django_pagination',
    'webstack_django_sorting',
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
    'django.middleware.locale.LocaleMiddleware',
    'linaro_django_pagination.middleware.PaginationMiddleware',
    'webstack_django_sorting.middleware.SortingMiddleware',
    'apps.users.middleware.RoleMiddleware',
    'njango.middleware.CalendarMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ROOT_URLCONF = 'awecounting.urls'

WSGI_APPLICATION = 'awecounting.wsgi.application'

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', gettext('English')),
    ('ne', gettext("Nepali")),
]

AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = '/'

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_L10N = True

USE_TZ = True

try:
    from .local_settings import *  # noqa
except ImportError:
    pass

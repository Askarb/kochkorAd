import environ
import os

import django.conf.locale
from django.utils.translation import gettext_lazy as _


root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False), )
environ.Env.read_env()

DEBUG = env('DEBUG', default=False)

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['kochkorcity.kg'])


INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'widget_tweaks',
    'webapp',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'webapp.middleware.WebappMiddleware',
]
if not DEBUG:
    INSTALLED_APPS += ['opbeat.contrib.django']

    OPBEAT = {
        'ORGANIZATION_ID': env('OPBEAT_ORGANIZATION_ID'),
        'APP_ID': env('OPBEAT_APP_ID'),
        'SECRET_TOKEN': env('OPBEAT_SECRET_TOKEN'),
    }

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('webapp', 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': env.db(),
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


LANGUAGES = [
    ('ky', _('Kyrgyz')),
    ('ru', _('Russian')),
    ('en', _('English')),
]

LANGUAGE_CODE = 'ru'


LOCALE_PATHS = (
    root('main', 'locale'),
    root('webapp', 'locale'),
)

EXTRA_LANG_INFO = {
    'ky': {
        'bidi': False, # right-to-left
        'code': 'ky',
        'name': 'Kyrgyz',
        'name_local': u'Кыргызча', #unicode codepoints here
    },
}

LANG_INFO = django.conf.locale.LANG_INFO.copy()
LANG_INFO.update(EXTRA_LANG_INFO)
django.conf.locale.LANG_INFO = LANG_INFO

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = root('staticfiles')
STATICFILES_DIRS = [
    root('static')
]

MEDIA_URL = '/media/'
if env('DEBUG'):
    MEDIA_ROOT = root('media')
else:
    MEDIA_ROOT = os.path.join('/mnt/media/kochkor')

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587


ADS_PER_PAGE = 10

TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')

INSTAGRAM_USERNAME = env('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = env('INSTAGRAM_PASSWORD')

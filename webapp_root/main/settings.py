import environ
import os

import django.conf.locale
from django.utils.translation import gettext_lazy as _


root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False), )
environ.Env.read_env()

DEBUG = env('DEBUG', default=False)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = '@o9eqyruv*%!!h6)8qgprd2xrn*03e+&d+dg3zb9e@03-kg6f2'

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
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
    'opbeat.contrib.django',
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

OPBEAT = {
    'ORGANIZATION_ID': env('OPBEAT_ORGANIZATION_ID', default=''),
    'APP_ID': env('OPBEAT_APP_ID', default=''),
    'SECRET_TOKEN': env('OPBEAT_SECRET_TOKEN', default=''),
}

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'webapp', 'templates'),
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

LANGUAGE_CODE = 'en-us'


LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'main', 'locale'),
    os.path.join(BASE_DIR, 'webapp', 'locale'),
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
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
if env('DEBUG'):
    MEDIA_ROOT = root('media')
else:
    MEDIA_ROOT = os.path.join('/mnt/media/kochkor')

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'kochkorjarnama@gmail.com'
EMAIL_HOST_PASSWORD = '1qaz@WSX28'
EMAIL_PORT = 587


ADS_PER_PAGE = 10

TELEGRAM_TOKEN = '462585305:AAHk_kLP2kZhpAIA47iKldJuS4sOeJpcYIk'
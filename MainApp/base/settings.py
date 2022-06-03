import os
from pathlib import Path
from config import Config

BASE_DIR = Path(__file__).resolve().parent.parent
BASE_FILES = os.path.join(BASE_DIR, "files")
BASE_DEV_FILES = os.path.join(BASE_DIR, "dev_files")

SECRET_KEY = Config.BASE_APP_SECRET_KEY

DEBUG = Config.DEBUG
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'api.apps.ApiConfig',
    'main.apps.MainConfig',
    'sign.apps.SignConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'files/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'base.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': Config.DB_NAME,
        'USER': Config.USERNAME,
        'PASSWORD': Config.PASSWORD,
        'HOST': Config.HOST,
        'PORT': Config.PORT,
    }
}
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_FILES, STATIC_URL[:-1])

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_FILES, MEDIA_URL[:-1])

STATICFILES_DIRS = (
    os.path.join(BASE_DEV_FILES, f"{STATIC_URL[:-1]}"),
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_TEMPLATE_PACK = 'bootstrap5'

LOGIN_URL = 'sign/login/'
LOGIN_REDIRECT_URL = '/'

# Custom user model
AUTH_USER_MODEL = 'main.UserModel'
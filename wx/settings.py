"""
Django settings for wx project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from apps.utils import consts

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'al_5odchumw51dflcr_wdne*8=hs-=derz*$e3=*^^n)y$qa&q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.250.12', '127.0.0.1', 'wx.huigo.com']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'xadmin',
    'crispy_forms',
    'reversion',
    'user',
    'api'
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
)

ROOT_URLCONF = 'wx.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'wx.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': consts.DB_NAME,
        'USER': consts.DB_USER,
        'PASSWORD': consts.DB_PASSWORD,
        'HOST': '192.168.250.12',
        # 'HOST': '127.0.0.1'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
# 线上部署的时候，用下面这句，方便apache2部署
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# 本地测试用下面这句，避免控制台404错误
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#################################  以下为手工添加的配置  ###################################

# cache
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': [
            '127.0.0.1:6379',
        ],

        "OPTIONS": {
            'DB': 1,
            "PASSWORD": "kgredis",
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        },
        "KEY_PREFIX": 'wx',
        "TIMEOUT": 480,

    },
}

# django-crontab任务加载
CRONJOBS = [
    # ('* * * * *', 'django.core.management.call_command', ['mycommand']),
    ('0 * * * *', 'api.cron.cron_get_token'),
    ('* * * * *', 'api.cron.cron_send_temp'),
    # ('20,40,59 * * * *', 'wxaccess.cron.get_access_token_job'),
]

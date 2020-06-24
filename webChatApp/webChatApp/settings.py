"""
Django settings for webChatApp project.

Based on 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
#import posixpath
from app.logUtil import logUtil
import datetime

# 保存するファイル名を指定
log_folder = '{0}.log'.format(datetime.date.today())
# ログの初期設定を行う
logger = logUtil.setup_logger(log_folder)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 # ログを出力
logger.debug("基本ディレクトリの設定:" + BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '336f49d7-fcbd-40f8-83cc-541661d926dd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

 # ログを出力
logger.debug("アプリケーションのインストール開始")
# Application references
# https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [
    'app',
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'channels_redis',
    'redis',
    'pyotp',
    'qrcode',
    'onetimepass',
]
 # ログを出力
logger.debug("アプリケーションのインストール終了")

 # ログを出力
logger.debug("Djangoミドルウェアの読み込み開始")
# Middleware framework
# https://docs.djangoproject.com/en/2.1/topics/http/middleware/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

 # ログを出力
logger.debug("Djangoミドルウェアの読み込み終了")

ROOT_URLCONF = 'webChatApp.urls'

 # ログを出力
logger.debug("テンプレート")

# Template configuration
# https://docs.djangoproject.com/en/2.1/topics/templates/
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'app/templates')],
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
 # ログを出力
logger.debug("１")

WSGI_APPLICATION = 'webChatApp.wsgi.application'
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 変更
        'NAME': 'chatdb', # プロジェクトで使用するデータベース名
        'USER': 'chatUser', # プロジェクトで使用するMySQLのユーザー名
        'PASSWORD': 'chatUser', # 同上。そのパスワード
    }
}

 # ログを出力
logger.debug("２")

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
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

 # ログを出力
logger.debug("３")

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

 # ログを出力
logger.debug("４")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
print(os.path.join(BASE_DIR, 'static'))

 # ログを出力
logger.debug("５")
ASGI_APPLICATION = 'webChatApp.routing.application'

 # ログを出力
logger.debug("６")
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

 # ログを出力
logger.debug("７")
LOGIN_URL = '/' 
LOGIN_REDIRECT_URL = '/chat/top'
#LOGIN_REDIRECT_URL = '/chat/2ash'
LOGOUT_REDIRECT_URL='/'

 # ログを出力
logger.debug("８")
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'yozakura780@gmail.com'
EMAIL_HOST_PASSWORD = 'yozakura9696'
EMAIL_USE_TLS = True

 # ログを出力
logger.debug("９")
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

 # ログを出力
logger.debug("１０")
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {  
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            #  choose file location of your liking
            'filename': os.path.normpath(os.path.join(BASE_DIR, 'logs/django.log')),  
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}  
"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
# 키분리 추가 코드
import os, json

from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
secret_file = os.path.join(BASE_DIR, 'secrets.json')

# 키분리 추가 코드
with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret("SECRET_KEY")

AUTH_USER_MODEL = 'users.User'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / 'templates'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

LOGIN_URL = '/users/login/'  # 변경된 URL

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []

# Application definition

# Email 전송
# 메일을 호스트하는 서버
EMAIL_HOST = 'smtp.gmail.com'

# gmail과의 통신하는 포트
EMAIL_PORT = '587'

# 발신할 이메일
# EMAIL_HOST_USER = '구글아이디@gmail.com'
EMAIL_HOST_USER = get_secret("EMAIL_HOST_USER")

# 발신할 메일의 비밀번호
# EMAIL_HOST_PASSWORD = '구글비밀번호'
EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")

# TLS 보안 방법
EMAIL_USE_TLS = True

# 사이트와 관련한 자동응답을 받을 이메일 주소
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# 비밀번호 초기화 이메일 템플릿 설정
PASSWORD_RESET_TIMEOUT = 600  # 비밀번호 초기화 요청의 유효시간 (초)
# PASSWORD_RESET_TIMEOUT_DAYS = 1  # 비밀번호 초기화 요청의 유효일수 (일)
PASSWORD_RESET_EMAIL_TEMPLATE_NAME = 'registration/password_reset_email.txt'

# crontab 설정. 잠시 보류
# CRONJOBS = [
# ('*/1 * * * *', 'users.tasks.delete_records'),  # 매 5분마다 테이블 레코드 삭제 작업 실행
# yourapp.models.YourModel' 부분을 삭제하려는 모델로 변경
#     ('*/1 * * * *', 'python manage.py sqlsequencereset users.models.VerificationCode'),  # 매일 자정에 모델 시퀀스 리셋
# ]

INSTALLED_APPS = [
    'posts',
    'users',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',
    'rest_framework',
    'corsheaders',  # corsheaders 앱 추가
    # 'django_crontab', # crontab 설정
    # 'django_extensions',# crontab 설정2
]

# CORS 설정 추가
CORS_ALLOW_ALL_ORIGINS = False  # 모든 오리진을 허용하지 않음
CORS_ALLOW_CREDENTIALS = True  # 자격증명(Credentials) 허용
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000',  # 허용하려는 오리진(Origin) 추가
    'http://10.100.104.13:8000',  # 다른 오리진(Origin)도 추가할 수 있음
    'http://10.100.104.13:8000',
]

# settings.py

# test
# test2
# 접근 목록자 , 임시로 전체 허용 했고,
ALLOWED_HOSTS = ['www.goldmagnetsoft.com']



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CorsMiddleware 추가
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = False

# 한국 현재 시간 설정시, False
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

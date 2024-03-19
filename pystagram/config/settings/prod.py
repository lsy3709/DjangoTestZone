import environ
import os

from .base import *

import django

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env(BASE_DIR / '.env')



ALLOWED_HOSTS = ['52.78.54.206','www.goldmagnetsoft.com','goldmagnetsoft.com']
# STATIC_ROOT = BASE_DIR / 'static/'
# STATICFILES_DIRS = []
DEBUG = False



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': '5432',
    }
}
# get_secret("SECRET_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ACCESS_KEY_ID = os.environ.get('AWS_S3_ACCESS_KEY_ID')
AWS_S3_SECRET_ACCESS_KEY = os.environ.get('AWS_S3_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')

if AWS_S3_ACCESS_KEY_ID and AWS_S3_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
    # 장고 4.2부터 스토리지 클래스 지정방법이 변경되었습니다.
    if django.VERSION < (4, 2):
        DEFAULT_FILE_STORAGE = "core.storages.aws.AwsMediaStorage"
        STATICFILES_STORAGE = "core.storages.aws.AwsStaticStorage"
    else:
        STORAGES = {
            "default": {
                "BACKEND": "core.storages.aws.AwsMediaStorage",
            },
            "staticfiles": {
                "BACKEND": "core.storages.aws.AwsStaticStorage",
            },
        }
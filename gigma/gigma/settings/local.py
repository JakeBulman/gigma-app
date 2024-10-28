from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gigma',
        'USER': 'gigma',
        'PASSWORD': 'gigma',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}

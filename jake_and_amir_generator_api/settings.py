"""
Django settings for jake_and_amir_generator_api project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


CHARACTER_DATA_DIR = "data/characters"
CHARACTER_WORDS = {}

from generator.MarkovGenerator import file_to_words

character_files = os.listdir(os.path.join(BASE_DIR, CHARACTER_DATA_DIR))
for character_file in character_files:
    character_words = file_to_words(os.path.join(BASE_DIR, CHARACTER_DATA_DIR, character_file))
    # drop the .txt extension to get the character name
    character_name = os.path.splitext(character_file)[0]

    CHARACTER_WORDS[character_name] = character_words


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "abc"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',

    'django_extensions',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
    )
}

ROOT_URLCONF = 'jake_and_amir_generator_api.urls'

WSGI_APPLICATION = 'jake_and_amir_generator_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www'


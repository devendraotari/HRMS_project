
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
from pathlib import Path

BASE_DIR_DEV = Path(__file__).resolve().parent.parent
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR_DEV / 'db.sqlite3',
    }
}


STATIC_URL = '/static/'



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

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ],
#      'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#  ),
# }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'


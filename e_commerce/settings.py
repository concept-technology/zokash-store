import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get('DEBUG', 'True').lower() in ['true', '1', 't']
ALLOWED_HOSTS = ['*','127.0.0.1', 'localhost', '10.0']
# DEBUG =True
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jazzmin',
    'django.contrib.admin',
    'gunicorn',
    'dj_database_url',
    "corsheaders",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',   
    'allauth.socialaccount.providers.facebook',   
    'allauth.socialaccount.providers.google',   
    'PIL',
    'widget_tweaks',
    'rest_framework',
    'crispy_forms',
    "crispy_bootstrap4",
    'django_countries',
    'paystack',
    'dotenv',
    'paystackapi',
    'my_store',
    'star_ratings',
    'django.contrib.humanize',
    'requests',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'e_commerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'e_commerce.wsgi.application'
database_url ='postgresql://zokash_household_db_user:uP97E5oviM7edStflqy0INmGj5PNFqgz@dpg-cq2acj3v2p9s73ep9stg-a.oregon-postgres.render.com/zokash_household_db'

if DEBUG:
    DATABASES = {
    'default': dj_database_url.config(
        default=database_url,
        conn_max_age=600,
    )
    }
else:
      DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
    )
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
USE_L10N = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    STATICFILES_STORAGE = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

JAZZMIN_SETTINGS = {
    "site_title": "zokash Admin",
    "site_header": "zokash household",
    "site_brand": "zokash household",
}

ACCOUNT_AUTHENTICATION_METHOD = "email"
LOGIN_REDIRECT_URL = 'store:index'
LOGOUT_REDIRECT_URL = 'store:index'
SIGNUP_REDIRECT_URL = 'store:index'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 1
}


SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() in ['true', '1', 't']
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

DEBUG_PROPAGATE_EXCEPTIONS = True

# Custom settings
STAR_RATINGS_STAR_HEIGHT = 20  # Height of each star in pixels
STAR_RATINGS_STAR_WIDTH = 20   # Width of each star in pixels
STAR_RATINGS_RERATE = False    # Users can only rate once
SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email'
        ],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}

CART_SESSION_ID = 'cart'

INTERNAL_IPS = [
    "127.0.0.1",
]

ACCOUNT_FORMS = {
    'add_email': 'allauth.account.forms.AddEmailForm',
    'change_password': 'allauth.account.forms.ChangePasswordForm',
    'login': 'allauth.account.forms.LoginForm',
    'reset_password': 'allauth.account.forms.ResetPasswordForm',
    'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
    'set_password': 'allauth.account.forms.SetPasswordForm',
    'signup': 'allauth.account.forms.SignupForm',
    'user_token': 'allauth.account.forms.UserTokenForm',
}

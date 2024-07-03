import os
from pathlib import Path
import dj_database_url

STAR_RATINGS_STAR_HEIGHT = 20  # Height of each star in pixels
STAR_RATINGS_STAR_WIDTH = 20   # Width of each star in pixels
STAR_RATINGS_RERATE = False    # Users can only rate once
SITE_ID=1

from dotenv import load_dotenv
load_dotenv()

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'Profile',
            'email'
        ],
        "AUTH_PARAMS":{'access-type':'online'}
    }
}


CART_SESSION_ID = 'cart'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-)_8%^jgfm$h(1pa=rv4m@6em#9rr1^n4^1rz$^5616o67!s99c'

# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ['*']


# Application definition

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
# ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]


SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1209600 

DAJAXICE_MEDIA_PREFIX = 'dajaxice'

CORS_ALLOW_ALL_ORIGINS: True

ROOT_URLCONF = 'e_commerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                # 'django.core.context_processors.request',
            ],
        },
    },
]

SECRET_KEY = 'django-insecure--z_2ma50$%ab+h24ef#bu_f_zsf4(d=d32$91dt8m6uh(!@9$!'
WSGI_APPLICATION = 'e_commerce.wsgi.application'

# PAYSTACK_SECRET_KEY = os.getenv('SECRET_KEY')
# PAYSTACK_PUBLIC_KEY = os.getenv('PUBLIC_KEY')

PAYSTACK_SECRET_KEY = 'sk_test_eef07558184af9678a899195eb8c0e705f986ff9'
PAYSTACK_PUBLIC_KEY = 'pk_test_ea75ece062f2a82f8f18506dbeff5f085a1ca58a'
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#      }
# }


DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default='postgresql://zokash_household_db_user:uP97E5oviM7edStflqy0INmGj5PNFqgz@dpg-cq2acj3v2p9s73ep9stg-a.oregon-postgres.render.com/zokash_household_db',
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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True
USE_L10N =True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

DEBUG = 'RENDER' not in os.environ.get('DEBUG')

# DEBUG = os.environ.get('DEBUG', default=True)


STATIC_URL = 'static/'
# STATICFILES_DIRS = [
#  os.path.join(BASE_DIR, 'static')
# ]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_HOST = os.environ.get('DJANGO_STATIC_HOST')

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    None
    
    
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
    
]

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "zokash Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "zokash household",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "zokash household",

    # Logo to use for your site, must be present in static files, used for brand on top left
    # "site_logo": "atinuke/zokashlogo.jpg",
}


ACCOUNT_AUTHENTICATION_METHOD = "email"
LOGIN_REDIRECT_URL ='store:index'
LOGOUT_REDIRECT_URL ='store:index'
SIGNUP_REDIRECT_URL ='store:index'
ACCOUNT_USERNAME_REQUIRED =False
ACCOUNT_LOGOUT_ON_GET =True
ACCOUNT_EMAIL_REQUIRED =True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
ACCOUNT_EMAIL_VERIFICATION = "none"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'samuelandrew145@gmail.com'
EMAIL_HOST_PASSWORD = '5804@gmail.coM'



REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 1
}










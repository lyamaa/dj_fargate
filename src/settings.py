import logging
from pathlib import Path
import environ
import requests

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# This code block is attempting to fetch the private IP address of the container running
# the Django application by making a request to the metadata URI. If successful, it adds
# the private IP address to the `ALLOWED_HOSTS` list, which allows the container to
# receive requests from that IP address. this is useful in a containerized environment
# where the IP address of the container may change dynamically. If the metadata request
# fails or the private IP address cannot be found, it logs an error message and does not
# add anything to the `ALLOWED_HOSTS` list.
PRIVATE_IP = None
METADATA_URI = env.get("METADATA_URI", default="")

try:
    res = requests.get(METADATA_URI)
    data = res.json()
    resp_meta_uri = data["containers"][0]
    PRIVATE_IP = resp_meta_uri["networks"][0]["ipv4Addresses"][0]
except Exception as e:
    logging.error(f"Error while fetching metadata: {e}")

if PRIVATE_IP:
    ALLOWED_HOSTS.append(PRIVATE_IP)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    "bankers",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "src.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "src.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # POSTGRES
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "fargate",
        "USER": "django",
        "PASSWORD": "helloNepal",
        "HOST": env("DB_HOST", default=""),
        "PORT": "5432",
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# These lines of code are configuring the settings for using Amazon S3 storage for
# static and media files in a Django project.
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default="")

AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default="")
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_s3_FILE_OVERWRITE = False


# only if django version >= 3.0
# `X_FRAME_OPTIONS = "SAMEORIGIN"` is a security measure that prevents the website from
# being embedded in an iframe on another website. It sets the `X-Frame-Options` header
# to `SAMEORIGIN`, which means that the website can only be embedded in an iframe on a
# page with the same origin (i.e. the same domain and protocol).
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])


# This code block is setting up secure SSL redirection and proxy SSL header settings for
# the Django project if the `DEBUG` setting is set to `False`. This is important for
# production environments where the website should be served over HTTPS for security
# reasons. The `SECURE_SSL_REDIRECT` setting ensures that all HTTP requests are
# redirected to HTTPS, while `SECURE_PROXY_SSL_HEADER` sets the header that should be
# used to determine whether the request was made over HTTPS or not.
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

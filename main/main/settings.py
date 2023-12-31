import os
from datetime import timedelta
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-pwbd0i+s=_e525gl*&f6i8&6ndf*iv2!^g3qm-bz3buo$5x#%("

DEBUG = True

ALLOWED_HOSTS = ["*", "127.0.0.0", "localhost", "0.0.0.0"]


DEFAULT_DJANGO = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

PROJECT_APPS = [
    "cars",
    "core",
    "comments",
]

THIRD_PARTY_LIBS = [
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "debug_toolbar",
    "mptt",
    "django_extensions",
]

INSTALLED_APPS = DEFAULT_DJANGO + PROJECT_APPS + THIRD_PARTY_LIBS

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Cars API",
    "DESCRIPTION": "The Cars API is a powerful tool that allows users to add, edit, view, and manage cars through a RESTful API interface. With this API, users can create and manage their own profiles, as well as add and edit cars with detailed information such as make, model, year, color, and more. The API also supports user authentication and authorization, ensuring that only authorized users can access and modify the data.Through this API, users can perform a wide range of tasks, from creating and deleting cars, to searching for specific cars by various attributes. The API also includes robust error handling and data validation, ensuring that all data entered is accurate and properly formatted.",
    "VERSION": "1.0.0",
    "COMPONENT_SPLIT_REQUEST": True,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=200),
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
INTERNAL_IPS = [
    "127.0.0.1",
]
ROOT_URLCONF = "main.urls"

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

WSGI_APPLICATION = "main.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "db",
        "PORT": 5432,
        "CONN_MAX_AGE": 600,
    }
}

# b = {
#     "default": dj_database_url.parse(
#         os.environ.get("DATABASE_URL"),
#         conn_max_age=600,
#         conn_health_checks=True,
#     )
# }

# for k, v in a["default"].items():
#     if a["default"][k] == b["default"][k]:
#         del b["default"][k]
# print("*****" * 10)
# print(b)


# print(a)

DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        # conn_health_checks=True,
    )
}


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
AUTH_USER_MODEL = "core.User"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CSRF_TRUSTED_ORIGINS = ["https://lobster-app-ku5vy.ondigitalocean.app"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


EMAIL_HOST = (os.environ.get("EMAIL_HOST"),)
EMAIL_PORT = (os.environ.get("EMAIL_PORT"),)
EMAIL_HOST_USER = (os.environ.get("EMAIL_HOST_USER"),)
EMAIL_HOST_PASSWORD = (os.environ.get("EMAIL_HOST_PASSWORD"),)
EMAIL_USE_TLS = (os.environ.get("EMAIL_USE_TLS"),)
EMAIL_USE_SSL = (os.environ.get("EMAIL_USE_SSL"),)
DEFAULT_FROM_EMAIL = (os.environ.get("DEFAULT_FROM_EMAIL"),)

PASSWORD_RESET_TIMEOUT = 60 * 60


DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda _request: DEBUG}

import hashlib
import os
from pathlib import Path

if os.environ.get("DOTENV", False):
    from dotenv import load_dotenv

    load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get(
    "SECRET_KEY", hashlib.sha256(os.urandom(24)).hexdigest()
)

DEBUG = os.environ.get("DEBUG", False)

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "backend",
    os.environ.get("DOMAIN_NAME", "127.0.0.1"),
    os.environ.get("EXTERNAL_IP"),
    f"{os.environ.get('DOMAIN_NAME', '127.0.0.1')}:8080",  # noqa: E231
    f"{os.environ.get('EXTERNAL_IP')}:8080",  # noqa: E231
    "127.0.0.1",
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework.authtoken",
    "rest_framework",
    "djoser",
    "django_filters",
    "drf_yasg",
    "core.apps.CoreConfig",
    "ingredient.apps.IngredientConfig",
    "recipe.apps.RecipeConfig",
    "user.apps.UserConfig",
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

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


if os.environ.get("USE_SQLITE", False) and os.environ.get("USE_SQLITE") != "0":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "django"),
            "USER": os.getenv("POSTGRES_USER", "django"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", 5432),
            "OPTIONS": {"options": "-c search_path=foodgram_schema,public"},
        }
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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


if os.environ.get("container", False):
    STATIC_URL = "/static_backend/"
    STATIC_ROOT = BASE_DIR / "static_backend"

    MEDIA_URL = "/media/"
    MEDIA_ROOT = "/static/media"
else:
    STATIC_URL = "/static_backend/"
    STATIC_ROOT = BASE_DIR / "static_backend"

    MEDIA_URL = "/media/"
    MEDIA_ROOT = STATIC_ROOT / "media"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "user.User"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "backend.pagination.APIPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}

DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_ID_FIELD": "id",
    "HIDE_USERS": False,
    "SERIALIZERS": {
        "user": "user.serializers.MyUserSerializer",
        "user_create": "user.serializers.CustomUserCreateSerializer",
        "current_user": "user.serializers.MyUserSerializer",
    },
    "PERMISSIONS": {
        "user": ["rest_framework.permissions.IsAuthenticated"],
        "user_list": ["rest_framework.permissions.AllowAny"],
    },
}

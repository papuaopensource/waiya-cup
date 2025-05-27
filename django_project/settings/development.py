from django_project.settings.base import *  # noqa: F403
from decouple import config


# https://docs.djangoproject.com/en/4.2/ref/settings/#std:setting-SECRET_KEY
SECRET_KEY = config("SECRET_KEY")

# https://docs.djangoproject.com/en/4.2/ref/settings/#debug
DEBUG = config("DEBUG", cast=bool)

# https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# https://docs.djangoproject.com/en/4.2/ref/settings/#installed-apps
INSTALLED_APPS += [  # noqa: F405
    # 3rd-party
    "django_browser_reload",
    "debug_toolbar",
]

# https://docs.djangoproject.com/en/4.2/ref/settings/#middleware
MIDDLEWARE += [  # noqa: F405
    # 3rd-party
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DATABASE"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    }
}

# https://docs.djangoproject.com/en/4.2/ref/settings/#media-url
MEDIA_URL = "/media/"

# https://docs.djangoproject.com/en/4.2/ref/settings/#media-root
MEDIA_ROOT = BASE_DIR / "mediafiles"  # noqa: F405

# https://docs.djangoproject.com/en/4.2/ref/settings/#static-root
STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa: F405

# https://docs.djangoproject.com/en/4.2/ref/settings/#static-url
STATIC_URL = "/static/"

# https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [BASE_DIR / "static"]  # noqa: F405

# https://docs.djangoproject.com/en/4.2/ref/settings/#internal-ips
INTERNAL_IPS = [
    "127.0.0.1",
]

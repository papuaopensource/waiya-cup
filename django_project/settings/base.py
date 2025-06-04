from pathlib import Path

from django.templatetags.static import static

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# https://docs.djangoproject.com/en/4.2/ref/settings/#installed-apps
INSTALLED_APPS = [
    # Third-party apps for django-unfold
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.humanize",  # Added for humanize filter
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # 3rd-party
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # 3rd-party
    "tailwind",
    "theme",
    # Local
    "core.apps.CoreConfig",
]

# https://docs.djangoproject.com/en/4.2/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # 3rd-party
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# https://docs.djangoproject.com/en/4.2/ref/settings/#root-urlconf
ROOT_URLCONF = "django_project.urls"

# https://docs.djangoproject.com/en/4.2/ref/models/fields/#bigautofield
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# https://docs.djangoproject.com/en/4.2/ref/settings/#wsgi-application
WSGI_APPLICATION = "django_project.wsgi.application"

# https://docs.djangoproject.com/en/4.2/ref/settings/#templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# https://docs.djangoproject.com/en/4.2/topics/i18n/
# https://docs.djangoproject.com/en/4.2/ref/settings/#language-code
LANGUAGE_CODE = "id-ID"

# https://docs.djangoproject.com/en/4.2/ref/settings/#time-zone
TIME_ZONE = "Asia/Jayapura"

# https://docs.djangoproject.com/en/4.2/ref/settings/#std:setting-USE_I18N
USE_I18N = True  # Mengaktifkan sistem internasionalisasi Django

# https://docs.djangoproject.com/en/4.2/ref/settings/#use-l10n
USE_L10N = True  # Mengaktifkan lokalalisasi format data

# https://docs.djangoproject.com/en/4.2/ref/settings/#use-tz
USE_TZ = True  # Mengaktifkan dukungan untuk pengaturan zona waktu

# https://whitenoise.readthedocs.io/en/latest/django.html
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# https://docs.djangoproject.com/en/4.2/ref/contrib/sites/#enabling-the-sites-framework
SITE_ID = 1

# https://unfoldadmin.com/docs/configuration/settings/
UNFOLD = {
    "SITE_TITLE": "Waiya CUP ∙ Dashboard",
    "SITE_HEADER": "Waiya CUP",
    "SITE_URL": "/",
    "SITE_SYMBOL": "view_apps",  # symbol from icon set
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("favicon/favicon.svg"),
        },
    ],
    "SHOW_BACK_BUTTON": True,
    "THEME": "light",
    "BORDER_RADIUS": "8px",
    "COLORS": {
        "base": {
            "50": "250, 250, 250",
            "100": "245, 245, 245",
            "200": "229, 229, 229",
            "300": "212, 212, 212",
            "400": "163, 163, 163",
            "500": "115, 115, 115",
            "600": "82, 82, 82",
            "700": "64, 64, 64",
            "800": "38, 38, 38",
            "900": "23, 23, 23",
            "950": "10, 10, 10",
        },
        "primary": {
            "50": "250, 250, 250",
            "100": "245, 245, 245",
            "200": "229, 229, 229",
            "300": "212, 212, 212",
            "400": "163, 163, 163",
            "500": "115, 115, 115",
            "600": "82, 82, 82",
            "700": "64, 64, 64",
            "800": "38, 38, 38",
            "900": "23, 23, 23",
            "950": "10, 10, 10",
        },
    },
}

# https://django-tailwind.readthedocs.io/en/latest/settings.html#tailwind-app-name
TAILWIND_APP_NAME = "theme"

from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-tiiu-university-secret-key-2024')

DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://localhost').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'uz-UZ'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Custom Admin UI ───────────────────────────────────────────────────────────
# (Jazzmin removed — custom templates used instead)
_REMOVED_JAZZMIN_SETTINGS = {
    "site_title": "TIIU Admin",
    "site_header": "TIIU",
    "site_brand": "TIIU",
    "site_logo": None,
    "login_logo": None,
    "login_logo_dark": None,
    "welcome_sign": "Xush kelibsiz, TIIU Boshqaruv Paneli",
    "copyright": "TIIU © 2026",
    "search_model": ["main.News", "main.Faculty", "main.Teacher"],
    "topmenu_links": [
        {"name": "🌐 Saytni ko'rish", "url": "/", "new_window": True},
        {"model": "auth.User"},
    ],
    "usermenu_links": [
        {"name": "Saytga o'tish", "url": "/", "new_window": True, "icon": "fas fa-external-link-alt"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [
        "main.SiteSettings",
        "main.Faculty",
        "main.Teacher",
        "main.Leadership",
        "main.Department",
        "main.News",
        "main.Event",
        "main.Gallery",
        "main.Partner",
        "main.FAQ",
        "main.ContactMessage",
        "main.Slider",
        "main.Center",
        "auth",
    ],
    "icons": {
        "auth":                  "fas fa-shield-alt",
        "auth.user":             "fas fa-user-circle",
        "auth.Group":            "fas fa-users",
        "main.SiteSettings":     "fas fa-cog",
        "main.Faculty":          "fas fa-graduation-cap",
        "main.Teacher":          "fas fa-chalkboard-teacher",
        "main.Leadership":       "fas fa-user-tie",
        "main.Department":       "fas fa-sitemap",
        "main.Center":           "fas fa-building",
        "main.News":             "fas fa-newspaper",
        "main.NewsCategory":     "fas fa-tags",
        "main.Event":            "fas fa-calendar-alt",
        "main.Gallery":          "fas fa-images",
        "main.GalleryImage":     "fas fa-image",
        "main.Slider":           "fas fa-sliders-h",
        "main.FAQ":              "fas fa-question-circle",
        "main.Partner":          "fas fa-handshake",
        "main.ContactMessage":   "fas fa-envelope",
    },
    "default_icon_parents":  "fas fa-chevron-right",
    "default_icon_children": "fas fa-dot-circle",
    "related_modal_active":  True,
    "custom_css": "css/admin_custom.css",
    "custom_js":  None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "language_chooser": False,
}

_REMOVED_JAZZMIN_UI_TWEAKS = {
    "navbar_small_text":          False,
    "footer_small_text":          True,
    "body_small_text":            False,
    "brand_small_text":           False,
    "brand_colour":               "navbar-dark",
    "accent":                     "accent-primary",
    "navbar":                     "navbar-dark",
    "no_navbar_border":           True,
    "navbar_fixed":               True,
    "layout_boxed":               False,
    "footer_fixed":               False,
    "sidebar_fixed":              True,
    "sidebar":                    "sidebar-dark-primary",
    "sidebar_nav_small_text":     False,
    "sidebar_disable_expand":     False,
    "sidebar_nav_child_indent":   True,
    "sidebar_nav_compact_style":  True,
    "sidebar_nav_legacy_style":   False,
    "sidebar_nav_flat_style":     True,
    "theme":                      "darkly",
    "default_theme_mode":         "dark",
    "button_classes": {
        "primary":   "btn-primary",
        "secondary": "btn-secondary",
        "info":      "btn-outline-info",
        "warning":   "btn-warning",
        "danger":    "btn-danger",
        "success":   "btn-success",
    },
}

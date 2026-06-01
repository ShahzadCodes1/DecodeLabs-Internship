"""
settings.py - Django Project Configuration
============================================
This file controls everything about how Django runs:
- Database configuration
- Installed apps
- Security settings
- Logging
- REST Framework settings

IMPORTANT: In production, sensitive values (SECRET_KEY, database passwords)
should come from environment variables, not be hardcoded here.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'
# BASE_DIR points to the folder containing manage.py
BASE_DIR = Path(__file__).resolve().parent.parent


# ===========================================================================
# SECURITY SETTINGS
# ===========================================================================

# SECURITY WARNING: keep the secret key used in production secret!
# In production, use: SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
SECRET_KEY = 'django-insecure-student-management-api-key-change-in-production-xyz123'

# SECURITY WARNING: don't run with debug turned on in production!
# When DEBUG=True, Django shows detailed error pages
DEBUG = True

# Hosts that are allowed to make requests to this server
# In production: ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
ALLOWED_HOSTS = ['*']  # Allow all hosts for development


# ===========================================================================
# INSTALLED APPS
# ===========================================================================

INSTALLED_APPS = [
    # Django's built-in apps
    'django.contrib.admin',         # Admin panel
    'django.contrib.auth',          # Authentication system
    'django.contrib.contenttypes',  # Content type framework
    'django.contrib.sessions',      # Session framework
    'django.contrib.messages',      # Messaging framework
    'django.contrib.staticfiles',   # Static file serving

    # Third-party apps
    'rest_framework',               # Django REST Framework ← THIS IS KEY

    # Our custom apps
    'students',                     # Our Student Management app
]


# ===========================================================================
# MIDDLEWARE
# ===========================================================================
# Middleware processes requests/responses before they hit views

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'student_management_api.urls'


# ===========================================================================
# TEMPLATES
# ===========================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'student_management_api.wsgi.application'


# ===========================================================================
# DATABASE CONFIGURATION
# ===========================================================================
# Using SQLite for development — simple, no setup needed.
# For production, switch to PostgreSQL:
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', 'student_db'),
#         'USER': os.environ.get('DB_USER', 'postgres'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', ''),
#         'HOST': os.environ.get('DB_HOST', 'localhost'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # db.sqlite3 file in the project root
    }
}


# ===========================================================================
# PASSWORD VALIDATION
# ===========================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ===========================================================================
# INTERNATIONALIZATION
# ===========================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True  # Store datetimes as UTC in the database


# ===========================================================================
# STATIC FILES
# ===========================================================================

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


# ===========================================================================
# DEFAULT PRIMARY KEY FIELD
# ===========================================================================
# This sets the default type for auto-generated primary keys
# BigAutoField = 64-bit integer (supports up to 9.2 quintillion records)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ===========================================================================
# DJANGO REST FRAMEWORK CONFIGURATION
# ===========================================================================
# This section configures how DRF behaves globally.

REST_FRAMEWORK = {
    # Default renderer: JSON (also includes browsable API for development)
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # Nice UI in browser
    ],

    # Default parser: accept JSON and form data
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],

    # Default pagination class
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    # Throttling — rate limiting (prevents API abuse)
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle',
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '100/day',
    #     'user': '1000/day',
    # },
}


# ===========================================================================
# LOGGING CONFIGURATION
# ===========================================================================
# Logging helps you debug issues in production by recording what happened.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {asctime} {message}',
            'style': '{',
        },
    },

    'handlers': {
        # Print logs to console (terminal)
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        # Write logs to a file
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'api.log',
            'formatter': 'verbose',
        },
    },

    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'students': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

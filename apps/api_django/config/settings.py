import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'insecure-dev-secret-key')
DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')
# Auto-add Render external host if present
RENDER_EXTERNAL_URL = os.getenv('RENDER_EXTERNAL_URL')
if RENDER_EXTERNAL_URL:
    try:
        from urllib.parse import urlparse
        parsed = urlparse(RENDER_EXTERNAL_URL)
        host = parsed.hostname
        if host and host not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(host)
    except Exception:
        pass

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'health',
    'api',
    'core',
    'finance',
    'market',
    'catalog',
    'epc',
    'governance',
    'consulting',
    'authz',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
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

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'true').lower() == 'true'
# Allowlist for production
_cors_allowed = os.getenv('CORS_ALLOWED_ORIGINS')
if _cors_allowed:
    CORS_ALLOWED_ORIGINS = [o.strip() for o in _cors_allowed.split(',') if o.strip()]
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOW_CREDENTIALS = True

# Allow specific origins via env when not allowing all
cors_allowed_origins_env = os.getenv('CORS_ALLOWED_ORIGINS', '')
if cors_allowed_origins_env:
    CORS_ALLOWED_ORIGINS = [o.strip() for o in cors_allowed_origins_env.split(',') if o.strip()]

# CSRF trusted origins from env and Render
CSRF_TRUSTED_ORIGINS = []
csrf_trusted_env = os.getenv('CSRF_TRUSTED_ORIGINS', '')
if csrf_trusted_env:
    CSRF_TRUSTED_ORIGINS.extend([o.strip() for o in csrf_trusted_env.split(',') if o.strip()])
if RENDER_EXTERNAL_URL:
    try:
        CSRF_TRUSTED_ORIGINS.append(RENDER_EXTERNAL_URL)
    except Exception:
        pass

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Media (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'



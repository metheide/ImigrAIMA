"""
Django settings for core project.
ImigrAIMA - Sistema de Gestão de Imigração
"""

from pathlib import Path
from django.contrib.messages import constants as messages
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s)f2!zftvd!8*-pqxz4k-v_&)ig6u-(9tel9g-(-bp28c$!ac)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # As minhas apps
    'website.apps.WebsiteConfig', # Usa a config bonita do apps.py
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # Deixar vazio pois estamos a usar templates dentro da app
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
LANGUAGE_CODE = 'pt-pt'
TIME_ZONE = 'Europe/Lisbon'
USE_I18N = True
USE_TZ = True

# --- Ficheiros Estáticos (CSS, JS, Imagens do Layout) ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'website/static',
]

# --- Ficheiros de Média (Uploads dos Utilizadores) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Limite de Upload (ex: 5MB) para não sobrecarregar
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880 

# --- Configurações de Login/Logout ---
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# --- Configuração de Mensagens (Bootstrap 5) ---
# Isto faz com que 'error' do Django use a cor 'danger' (Vermelho) do Bootstrap
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.DEBUG: 'secondary',
    messages.INFO:  'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
}

# Configuração Padrão de Chaves Primárias
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
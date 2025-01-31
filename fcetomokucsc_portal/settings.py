from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()



BASE_DIR = Path(__file__).resolve().parent.parent


AUTH_USER_MODEL = 'career_app.CustomUser'


AUTHENTICATION_BACKENDS = [
    'career_app.authentication.EmailVerifiedBackend',  # Use the custom backend
    'django.contrib.auth.backends.ModelBackend',  # Default backend
]

# Static and media files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'career_app/static')]
 
STATIC_ROOT = BASE_DIR / 'staticfiles'

LOGIN_URL = 'career_app/login'  

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
LOGIN_URL = 'career_app/login'
LOGIN_REDIRECT_URL = 'career_app/home'
LOGOUT_REDIRECT_URL = 'career_app/login'



# Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Ensure this is defined correctly

ROOT_URLCONF = 'fcetomokucsc_portal.urls'

# Installed apps and middleware
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'career_app',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', 
   
]

 
# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', 5432),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SITE_ID = 1

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('SMTP_SERVER', 'in_v3.mailjet.com')
EMAIL_PORT = int(os.getenv('PORT', 465))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('MAILJET_API_KEY')
EMAIL_HOST_PASSWORD = os.getenv('MAILJET_SECRET_KEY')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

MAILJET_API_KEY =  os.getenv('MAILJET_API_KEY')
MAILJET_SECRET_KEY = os.getenv('MAILJET_SECRET_KEY')


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field


LOGIN_URL = 'career_app/login'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST="smtp.gmail.com"
# EMAIL_PORT=465
# EMAIL_USE_SSL=True
# EMAIL_HOST_USER="ssesconf2024@gmail.com"
# EMAIL_HOST_PASSWORD="wkfe ulxx tjqt oivt"
# DEFAULT_FROM_EMAIL="ssesconf2024@gmail.com"
# DEFAULT_FROM_USER = "FCETOMOKUCSC <ssesconf2024@gmail.com>"



# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'career_app/templates')],
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
 
# Other configurations
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


DEBUG = True
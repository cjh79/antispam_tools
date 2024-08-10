import os

SECRET_KEY = 'secret'

DIRNAME = os.path.dirname(__file__)

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }
}

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
)

STATIC_URL = '/static/'

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

AKISMET_API_KEY = ''
AKISMET_SITE_URL = 'ride.guru'
AKISMET_TEST_MODE = False
RECAPTCHA_SITEKEY = ''
RECAPTCHA_SECRETKEY = ''
RECAPTCHA_WIDGET = 'antispam.captcha.widgets.ReCAPTCHA'
RECAPTCHA_TIMEOUT = 5
RECAPTCHA_PASS_ON_ERROR = False
RECAPTCHA_TEST_MODE = False

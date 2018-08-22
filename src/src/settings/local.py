from .base import *             # noqa
import sys
import logging.config


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

INTERNAL_IPS = ['127.0.0.1']

# Turn off debug while imported by Celery with a workaround
# See http://stackoverflow.com/a/4806384
if 'celery' in sys.argv[0]:
    DEBUG = False

# Django Debug Toolbar
INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


# Show emails to console in DEBUG mode
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = 'True'
EMAIL_POST = '587'


# Log everything to the logs directory at the top
LOGFILE_ROOT = os.path.join(BASE_DIR, 'logs')


# Reset logging
# http://www.caktusgroup.com/blog/2015/01/27/
# Django-Logging-Configuration-logging_config-default-settings-logger/


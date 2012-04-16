# Django settings for progcomp project.
# These values should be satisfactory for a local testing environment
# See settings_server.py.example for additional documentation
import re
import datetime

DEBUG = True
TEMPLATE_DEBUG = DEBUG
USING_NGINX = False

PROFILER = True
PROFILER_FILTERS = (
    re.compile(r'.*stats$'),
    re.compile(r'^django\.views\.static\.serve'),
    re.compile(r'^debug_toolbar.*'),
)

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.sqlite3',
        'NAME':     '../database/progcomp.db',
        'USER':     '',
        'PASSWORD': '',
        'HOST':     '',
        'PORT':     '',
    },
}


MEDIA_ROOT = '../media/'
MEDIA_URL  =  '/media/'   # This is necessary for nginx to forward from

USERS_ROOT = MEDIA_ROOT+'users/'
USERS_URL = '/user/' # Django will handle user requests through this URI

STATIC_ROOT = '../static/'
STATIC_URL = '/static'

TEMPLATE_DIRS = ('../templates',)

LOGIN_REDIRECT_URL = '/account/'
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'

GRADE_DIR = '../grader/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Make this unique, and don't share it with anybody.
SECRET_KEY = '6(_q&p0gss%6ddr1(+mm+fxbsd(4o+54tmmv^b82pb+58(j+r@'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.load_template_source',
)

# These are used to make some context globally accessible
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'progcomp.context_processors.profiler',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'progcomp.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'progcomp.problems',
    'progcomp.submission',
    'progcomp.account',
    'progcomp.judge',
    'progcomp.pretty_times',
    'progcomp',
)

INTERNAL_IPS = ()

LOG_FILE = "../error_log.txt"
LOG_FILE_MAXSIZE = 2**30 # 1 GB
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'error_fmt': {
            'format': '\n%(asctime)s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'error_handler': {
            'class': 'logging.handlers.RotatingFileHandler',#'log.ErrorHandler'
            'maxBytes': LOG_FILE_MAXSIZE,
            'backupCount': 1,
            'filename': LOG_FILE,
            'formatter': 'error_fmt',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['error_handler'],
            'propagate': True,
        },
    },
}
IGNORABLE_404_URLS = (
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
)

RESUME_TYPES = ['text/plain', 'application/pdf']

# Amount of time a person has to upload the result of attempt, in seconds.
ATTEMPT_DURATION = 120

# Competition time window; you should use datetime.datetime(...) in production
START = datetime.datetime.now() - datetime.timedelta(hours=1)
END   = datetime.datetime.now() + datetime.timedelta(hours=1)

# Dates for graduation drop down
GRAD_DATES = [
    datetime.date(2011, 12, 1),
    datetime.date(2012, 5, 1),
    datetime.date(2012, 8, 1),
    datetime.date(2012, 12, 1),
    datetime.date(2013, 5, 1),
    datetime.date(2013, 8, 1),
    datetime.date(2013, 12, 1),
    datetime.date(2014, 5, 1),
    datetime.date(2014, 8, 1),
    datetime.date(2014, 12, 1),
    datetime.date(2015, 5, 1),
    datetime.date(2015, 8, 1),
    datetime.date(2015, 12, 1),
    datetime.date(2016, 5, 1),
    datetime.date(2016, 8, 1),
    datetime.date(2016, 12, 1),
    datetime.date(2017, 5, 1),
    datetime.date(2017, 8, 1),
    datetime.date(2017, 12, 1),
]

DEFAULT_FROM_EMAIL = 'no-reply@progcomp.upe.cs.rpi.edu'

# Undocumented / possibly unused
ADMINS = ()
MANAGERS = ADMINS
ADMIN_MEDIA_PREFIX = '/adminmedia/'
SITE_ID = 1
AUTH_PROFILE_MODULE = "register.Profile"

import os
if os.path.isfile('settings_server.py'):
  from settings_server import *

# Post-import commands
# Include debug_toolbar if debug mode is enabled
if DEBUG:
    INSTALLED_APPS += ('progcomp.debug_toolbar',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INTERNAL_IPS += ('127.0.0.1',)

if PROFILER:
    INSTALLED_APPS += ('progcomp.stats',)
    MIDDLEWARE_CLASSES += ('progcomp.stats.middleware.ProfilingMiddleware',)


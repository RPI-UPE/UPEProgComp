
# Django settings for progcomp project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = '/home/progcomp/progcomp/database/progcomp.db'             # Or path to database file if using sqlite3.

DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = 'US/Eastern'
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

MEDIA_ROOT = '/home/progcomp/progcomp/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

MEDIA_URL = 'http://stonelinks.org/media/'

STATIC_URL = 'http://stonelinks.org/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/adminmedia/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '6(_q&p0gss%6ddr1(+mm+fxbsd(4o+54tmmv^b82pb+58(j+r@'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'progcomp.urls'

TEMPLATE_DIRS = (
    '/home/progcomp/progcomp/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'progcomp.problems',
    'progcomp.submission',
    'progcomp.scoreboard',
    'progcomp.account',
    'progcomp.judge',
    'progcomp',
)

AUTH_PROFILE_MODULE = "register.Profile"

RESUME_TYPES = ['text/plain', 'application/pdf']

LOGIN_REDIRECT_URL = '/account/'
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'
MAX_REGISTRATIONS = 60

import datetime
START = datetime.datetime(2012, 3, 31, 12, 10)
END   = datetime.datetime(2012, 3, 31, 15, 00)
#START = datetime.datetime(2012, 3, 1, 12, 10)
#END   = datetime.datetime(2012, 3, 31, 15, 25)

#Amount of time a person has to upload the result of attempt, in seconds.
ATTEMPT_DURATION = 120

GRAD_DATES = [
        datetime.datetime(2011, 12, 1),
        datetime.datetime(2012, 5, 1),
        datetime.datetime(2012, 8, 1),
        datetime.datetime(2012, 12, 1),
        datetime.datetime(2013, 5, 1),
        datetime.datetime(2013, 8, 1),
        datetime.datetime(2013, 12, 1),
        datetime.datetime(2014, 5, 1),
        datetime.datetime(2014, 8, 1),
        datetime.datetime(2014, 12, 1),
        datetime.datetime(2015, 5, 1),
        datetime.datetime(2015, 8, 1),
        datetime.datetime(2015, 12, 1),
        datetime.datetime(2016, 5, 1),
        datetime.datetime(2016, 8, 1),
        datetime.datetime(2016, 12, 1),
        datetime.datetime(2017, 5, 1),
        datetime.datetime(2017, 8, 1),
        datetime.datetime(2017, 12, 1)
]

GRADE_DIR = '../grader/'

DEFAULT_FROM_EMAIL = 'no-reply@progcomp.upe.cs.rpi.edu'

import os
if os.path.isfile('local_settings.py'):
  from local_settings import *

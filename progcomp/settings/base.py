# Django base settings for progcomp project.
import re
import datetime

# Path configuration
# Note that many of these will work for production and devel but can be
# overridden as needed.

# MEDIA_ROOT sets the directory where uploaded files will be stored
# MEDIA_URL is not used for direct access, but instead for passing paths to
# nginx so that it can serve files from there
MEDIA_ROOT = 'media/'
MEDIA_URL  =  '/media/'

# USERS_ROOT contains folders for each user created and stores diffs and input
# sets for their use. USERS_URL is the relative or absolute URI that Django will
# use to read the users directory (see progcomp/urls.py). THIS IS NOT THE
# DIRECTORY ITSELF.
USERS_ROOT = MEDIA_ROOT+'users/'
USERS_URL = '/user/'

# STATIC_ROOT and STATIC_URL describe where the static files (css, js, images,
# etc.) are stored and how they should be accessed via the browser,
# respectively. Check progcomp/urls.py for forwarding information regarding the
# latter.
STATIC_ROOT = 'static'
STATIC_URL = '/static/'
STATICFILES_DIRS = ('app/static',)

# Path on server to the directory containing templates. Make sure that the below
# is in tuple form, i.e., TEMPLATE_DIRS = ('path',)
TEMPLATE_DIRS = ('progcomp/templates',)

# URL redirects for user class
LOGIN_REDIRECT_URL = '/account/'
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'

# Location of inputs and outputs
GRADE_DIR = 'grader/'

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
    'django.template.loaders.app_directories.Loader',
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
    'django.contrib.staticfiles',
    'progcomp.problems',
    'progcomp.scoreboard',
    'progcomp.submission',
    'progcomp.account',
    'progcomp.judge',
    'progcomp',
    'progcomp.stats',
)

INTERNAL_IPS = ()

# File to log all server errors and 404 errors to; when LOG_FILE_MAX_SIZE is
# reached (in bytes), it is moved to a backup as <name>.1 and a new file is
# created. Only two files will exist at any given time.
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

# Dates for graduation drop down -- May, August, and December are all valid months
today = datetime.date.today()
GRAD_DATES = filter(lambda x: x > today,
    [datetime.date(y, m, 1) for y in xrange(today.year, today.year+6) for m in [5, 8, 12]])

# Allows use of <User>.get_profile()
AUTH_PROFILE_MODULE = 'account.Profile'

# Required for admin css/js
ADMIN_MEDIA_PREFIX = '/adminmedia/'

# Undocumented / possibly unused
ADMINS = ()
MANAGERS = ADMINS
SITE_ID = 1

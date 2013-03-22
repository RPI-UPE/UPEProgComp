# Django settings for progcomp development server
# Any values set in here will override default values found in base.py
from progcomp.settings.base import *

# DEBUG should always be False in a production environment
# This controls whether detailed error messages are output to the user, which
# may contain sensitive information.
DEBUG = True
TEMPLATE_DEBUG = DEBUG
# For debugging
INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INTERNAL_IPS += ('127.0.0.1',)

# USING_NGINX is a flag used by the 'user' controller to decide whether to use
# header information to let nginx send file contents to the browser or to use
# Django's static.serve. This should be true in a production environment if
# nginx is installed.
USING_NGINX = False

# The profiler can be enabled here, but it also requires debug mode to view the
# results page. Be warned that it requires a bit of overhead to log information.
PROFILER = True
PROFILER_FILTERS = (
    re.compile(r'.*stats$'),
    re.compile(r'^django\.views\.static\.serve'),
    re.compile(r'^debug_toolbar.*'),
)
MIDDLEWARE_CLASSES += ('progcomp.stats.middleware.ProfilingMiddleware',)

# Configure the database engine and login information
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.sqlite3',
        'NAME':     'database/progcomp.db',
        # The following are not used with sqlite3
        'USER':     '',
        'PASSWORD': '',
        'HOST':     '',
        'PORT':     '',
    },
}

# Devel just uses local memory cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 60,
    },
}

# Emails sent from the server come from here
DEFAULT_FROM_EMAIL = 'Progcomp Devel <no-reply@localhost>'

# Competition time window; you should use datetime.datetime(...) in production
START = datetime.datetime.now() - datetime.timedelta(hours=1)
END   = datetime.datetime.now() + datetime.timedelta(hours=1)

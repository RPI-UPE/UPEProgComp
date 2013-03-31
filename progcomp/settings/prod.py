# Django settings for progcomp production server
# Any values set in here will override default values found in base.py
import os
import datetime
import dj_database_url
from progcomp.settings.base import *

ALLOWED_HOSTS = os.getenv('DJANGO_DNS_HOSTS').split(' ')

# Make this unique, and don't share it with anybody. Stored in the environment.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# DEBUG should always be False in a production environment
# This controls whether detailed error messages are output to the user, which
# may contain sensitive information.
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# USING_NGINX is a flag used by the 'user' controller to decide whether to use
# header information to let nginx send file contents to the browser or to use
# Django's static.serve. This should be true in a production environment if
# nginx is installed.
USING_NGINX = True

# The profiler can be enabled here, but it also requires debug mode to view the
# results page. Be warned that it requires a bit of overhead to log information.
PROFILER = False
PROFILER_FILTERS = ( )

# Configure the database engine and login information
# We store this information as a connection string in the environment variables
# ex: postgres://user:pass@hostname:database
DATABASES = { 'default': dj_database_url.config() }

# Configure the caching mechanism: comment this block out if you cannot setup Memcached
# Note that there is no ability to invalidate the cache if you do not use
# memcached, so the timeout will be defaulted to 60s
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211', # Default memcached port
        'TIMEOUT': 60 * 10,
    },
}

# Emails sent from the server come from here
DEFAULT_FROM_EMAIL = 'UPE Progcomp <no-reply@progcomp.upe.cs.rpi.edu>'

try:
  from progcomp.settings.competition import START, END
except Exception as e:
  print "Could not import competition times. Make sure you have created a progcomp/settings/competition.py file containing START and END dates"
  raise e

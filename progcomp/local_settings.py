
# Django settings for progcomp project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '../database/progcomp.db',            # Or path to database file if using sqlite3.
        'USER': '',            # Not used with sqlite3.
        'PASSWORD': '',        # Not used with sqlite3.
        'HOST': '',            # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',            # Set to empty string for default. Not used with sqlite3.
    },
}

MEDIA_ROOT = '../media/'
USERS_ROOT = MEDIA_ROOT+'users/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

MEDIA_URL = 'http://127.0.0.1:8000/media/'
USERS_URL = 'http://127.0.0.1:8000/media/users/'

STATIC_ROOT = '../static/'
STATIC_URL = '/css_static'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/adminmedia/'

TEMPLATE_DIRS = (
    '../templates',
)

import datetime
START = datetime.datetime(2012, 3, 31, 12, 10)
END   = datetime.datetime(2012, 5, 1, 15, 00)

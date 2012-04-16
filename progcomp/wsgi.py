import os
import sys
import site

site.addsitedir('/usr/lib/python2.7/site-packages')

sys.path.append('/www/UPEProgComp')

os.environ['DJANGO_SETTINGS_MODULE'] = 'progcomp.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

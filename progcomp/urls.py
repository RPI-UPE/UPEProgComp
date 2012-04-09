from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'progcomp.views.index', name='home'),
    (r'^user/', include('progcomp.user.urls')),
    (r'^account/', include('progcomp.account.urls')),
    (r'^submit/', include('progcomp.submission.urls')),
    (r'^scoreboard/', include('progcomp.scoreboard.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    # This should be handled in production by nginx
    url(r'^static/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.STATIC_ROOT,'show_indexes': True}),
)


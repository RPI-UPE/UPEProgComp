from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'progcomp.views.index', name='home'),
    url(r'^rules$', 'progcomp.views.rules', name='rules'),
    url(r'^contact/$', 'progcomp.views.contact', name='contact'),
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

if settings.PROFILER:
    urlpatterns += patterns('',
        (r'^stats/', include('progcomp.stats.urls')),
    )

if not settings.USING_NGINX:
    urlpatterns += patterns('',
        # This should be handled in production by nginx
        url(r'^static/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.STATIC_ROOT,'show_indexes': True}),
        url(r'^(?P<path>favicon.ico)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,'show_indexes': False}),
    )

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'progcomp.views.index', name='home'),
    (r'^account/', include('account.urls')),
    (r'^submit/', include('progcomp.submission.urls')),
    (r'^judge/', include('progcomp.judge.urls')),
    (r'^scoreboard/', include('progcomp.scoreboard.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^vanguard/$', 'direct_to_template', {'template': 'vanguard.html'}),
)

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    url(r'^css_static/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.STATIC_ROOT,'show_indexes':True}),
)


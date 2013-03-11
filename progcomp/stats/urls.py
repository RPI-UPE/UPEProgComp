from django.conf.urls import *

urlpatterns = patterns('progcomp.stats.views',
    url(r'^reset/$', 'reset', name='reset-stats'),
    url(r'', 'index', name='stats'),
)


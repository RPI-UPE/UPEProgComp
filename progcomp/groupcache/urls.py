from django.conf.urls.defaults import *


urlpatterns = patterns(
    'groupcache.views',
    (r'^groupcachetest/(?P<title>\w+)/$', 'groupcachetest'),
    )

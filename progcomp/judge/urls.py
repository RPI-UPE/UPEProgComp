from django.conf.urls.defaults import *


urlpatterns = patterns('progcomp.judge.views',
    url(r'^$', 'judge', name='judge'),
)

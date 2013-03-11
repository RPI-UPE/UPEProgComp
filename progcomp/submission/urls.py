from django.conf.urls import *


urlpatterns = patterns('progcomp.submission.views',
    url(r'^download/$', 'download', name='download'),
    url(r'^json$', 'json'),
    url(r'^(\d+)/$', 'submit', name='submit'),
    url(r'^(\d+)/refresh/$', 'refresh', name='refresh'),
)

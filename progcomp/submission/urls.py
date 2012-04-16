from django.conf.urls.defaults import *


urlpatterns = patterns('progcomp.submission.views',
	url(r'^download$', 'download', name='download'),
    url(r'^(\d+)$', 'submit', name='submit'),
    url(r'^(\d+)/refresh$', 'refresh', name='refresh'),
)

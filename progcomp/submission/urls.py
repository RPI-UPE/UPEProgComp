from django.conf.urls.defaults import *


urlpatterns = patterns('progcomp.submission.views',
	url(r'^download$', 'download', name='download'),
    url(r'^$', 'submit', name='submit'),
    url(r'^(\d+)$', 'submit', name='submit'),
)

from django.conf.urls.defaults import *


urlpatterns = patterns('progcomp.submission.views',
	url(r'^download$', 'download', name='download'),
    url(r'^$', 'submit', name='submit'),
    url(r'^success/$', 'success', name='submit-success'),
    url(r'^failure/$', 'failure', name='submit-failure'),
    url(r'^too_late/$', 'too_late', name='too_late'),
)

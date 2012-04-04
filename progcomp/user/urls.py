from django.conf.urls.defaults import *

urlpatterns = patterns('progcomp.user.views',
    url(r'input/(\w+)$', 'input'),
    url(r'diff/(\d+)$', 'diff'),
)

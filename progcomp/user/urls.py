from django.conf.urls.defaults import *

urlpatterns = patterns('progcomp.user.views',
    url(r'input/(\w+)/$', 'input'),
    url(r'input/(\w+)\.in$', 'input', kwargs={'direct':True}),
    url(r'diff/(\d+)/$', 'diff'),
    url(r'diff/(\d+)/tiny/$', 'diff', kwargs={'tiny':True}),
)

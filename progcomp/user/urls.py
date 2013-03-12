from django.conf.urls import *

urlpatterns = patterns('progcomp.user.views',
    url(r'^input/(\w+)/$', 'input', name='input'),
    url(r'^input/(\w+)\.in$', 'input', kwargs={'direct':True}, name='input_direct'),
    url(r'^diff/(\d+)/$', 'diff', name='diff'),
    url(r'^diff/(\d+)/tiny/$', 'diff', kwargs={'tiny':True}),
    url(r'^resume/?$', 'resume', name='resume'),
    url(r'^(\d+)/resume/([0-9A-Fa-f]+)?$', 'resume', name='resume'),
)

from django.conf.urls import *

urlpatterns = patterns('progcomp.user.views',
    # Sample input files
    url(r'^input/sample/$', 'sample_input', name='sample_input'),
    url(r'^input/sample\.in$', 'sample_input', kwargs={'direct':True}, name='sample_input_direct'),

    # Without number -- assume self
    url(r'^input/(?P<slug>\w+)/$', 'input', name='input'),
    url(r'^diff/(\d+)/$', 'diff', name='diff'),
    url(r'^diff/(\d+)/tiny/$', 'diff', kwargs={'tiny':True}),
    url(r'^resume/?$', 'resume', name='resume'),

    # With number -- does not require auth to access
    url(r'^(?P<user_id>\d+)/input/(?P<slug>\w+)\.in$', 'input', kwargs={'direct':True}, name='input_direct'),
    url(r'^(\d+)/resume/([0-9A-Fa-f]+)?$', 'resume', name='resume'),
)

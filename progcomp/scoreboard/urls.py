from django.conf.urls.defaults import *


urlpatterns = patterns('progcomp.scoreboard.views',
    url(r'^$', 'scoreboard', name='scoreboard'),
    url(r'^results/$', 'results'),
)

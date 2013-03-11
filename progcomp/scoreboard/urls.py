from django.conf.urls import *


urlpatterns = patterns('progcomp.scoreboard.views',
    url(r'^$', 'scoreboard', name='scoreboard'),
    url(r'^results/$', 'results'),
)

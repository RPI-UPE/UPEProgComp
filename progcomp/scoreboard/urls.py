from django.conf.urls import *


urlpatterns = patterns('progcomp.scoreboard.views',
    url(r'^([0-9A-Fa-f]{10})?$', 'scoreboard', name='scoreboard'),
)

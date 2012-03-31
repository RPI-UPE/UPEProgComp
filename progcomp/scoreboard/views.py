import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from progcomp.scoreboard.models import Scoreboard


@login_required
def scoreboard(request, template='scoreboard/scoreboard.html'):
    context = {}
    context['scoreboards'] = Scoreboard.objects.all()
    context['is_ended'] = datetime.datetime.now() > settings.END
    return render_to_response(template, context,
            context_instance=RequestContext(request))
